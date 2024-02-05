def wallet_create_handler(sender, instance, created, **kwargs):
    if created:
        instance.wallet.objects.create(balance=0)

