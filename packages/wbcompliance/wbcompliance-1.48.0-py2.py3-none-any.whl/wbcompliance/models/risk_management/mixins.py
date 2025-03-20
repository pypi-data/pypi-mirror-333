from datetime import date
from typing import Any

from django.contrib.contenttypes.models import ContentType
from django.db import models, transaction
from django.utils.functional import cached_property

from .checks import RiskCheck, evaluate_as_task
from .rules import RiskRule


class RiskCheckMixin(models.Model):
    """
    A utility mixin to inherit from when a model proposes a risk check workflow on one of its field
    """

    id: int

    @property
    def checked_object(self) -> Any:
        raise NotImplementedError()

    @property
    def check_evaluation_date(self) -> Any:
        raise NotImplementedError()

    @cached_property
    def checked_object_content_type(self) -> ContentType:
        return ContentType.objects.get_for_model(self.checked_object)

    @property
    def checks(self) -> models.QuerySet[RiskCheck]:
        """
        Returned the check triggered by this object (self)
        Returns: A queryset of RiskCheck
        """
        return RiskCheck.objects.filter(
            checked_object_content_type=self.checked_object_content_type,
            checked_object_id=self.checked_object.id,
            evaluation_date=self.check_evaluation_date,
        )

    @cached_property
    def has_assigned_active_rules(self) -> bool:
        """
        Return True if an enabled and active rule is available for the assigned checked object
        """
        return RiskRule.objects.get_active_rules_for_object(self.checked_object)

    @property
    def has_all_check_completed_and_succeed(self) -> bool:
        """
        Return True if checks are available and they all succeed
        """
        return (
            self.checks.exists()
            and not self.checks.exclude(
                status__in=[RiskCheck.CheckStatus.SUCCESS, RiskCheck.CheckStatus.WARNING]
            ).exists()
        )

    @property
    def has_all_check_completed(self) -> bool:
        """
        Return True if checks are available and they all succeed
        """
        return (
            self.checks.exists()
            and not self.checks.filter(
                status__in=[RiskCheck.CheckStatus.RUNNING, RiskCheck.CheckStatus.PENDING]
            ).exists()
        ) or not self.checks.exists()

    @property
    def has_no_rule_or_all_checked_succeed(self) -> bool:
        return (
            self.has_assigned_active_rules and self.has_all_check_completed_and_succeed
        ) or not self.has_assigned_active_rules

    def get_worst_check_status(self) -> RiskCheck.CheckStatus:
        status_ordered = [
            RiskCheck.CheckStatus.FAILED,
            RiskCheck.CheckStatus.WARNING,
            RiskCheck.CheckStatus.RUNNING,
            RiskCheck.CheckStatus.PENDING,
        ]
        for status in status_ordered:
            if self.checks.filter(status=status).exists():
                return status
        return RiskCheck.CheckStatus.SUCCESS

    def evaluate_active_rules(self, evaluation_date: date, *dto, asynchronously: bool = True):
        for rule in RiskRule.objects.get_active_rules_for_object(self.checked_object):
            check = RiskCheck.objects.update_or_create(
                rule=rule,
                evaluation_date=evaluation_date,
                checked_object_content_type=self.checked_object_content_type,
                checked_object_id=self.checked_object.id,
                defaults={"status": RiskCheck.CheckStatus.PENDING},
            )[0]
            if asynchronously:
                transaction.on_commit(
                    lambda: evaluate_as_task.delay(
                        check.id, *dto, override_incident=True, ignore_informational_threshold=True
                    )
                )
            else:
                check.evaluate(*dto, override_incident=True, ignore_informational_threshold=True)

    class Meta:
        abstract = True
