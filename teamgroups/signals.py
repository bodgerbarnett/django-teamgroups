from django.dispatch import Signal


invitation_sent = Signal(providing_args=['instance'])
