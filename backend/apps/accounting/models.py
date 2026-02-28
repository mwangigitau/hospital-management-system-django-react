from django.db import models

from utils.models import BranchScopedModel


class LedgerAccount(BranchScopedModel):
    ACCOUNT_TYPES = [('asset', 'Asset'), ('liability', 'Liability'), ('income', 'Income'), ('expense', 'Expense')]

    code = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=150)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)

    def __str__(self):
        return f'{self.code} - {self.name}'


class JournalEntry(BranchScopedModel):
    reference = models.CharField(max_length=100, blank=True)
    narration = models.TextField(blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    debit_account = models.ForeignKey(LedgerAccount, on_delete=models.PROTECT, related_name='debit_entries')
    credit_account = models.ForeignKey(LedgerAccount, on_delete=models.PROTECT, related_name='credit_entries')
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'JE {self.id}'
