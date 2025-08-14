from django.core.management.base import BaseCommand
from django.contrib.sessions.models import Session
from django.utils import timezone


class Command(BaseCommand):
    help = 'Limpia todas las sesiones activas - útil para desarrollo'

    def add_arguments(self, parser):
        parser.add_argument(
            '--all',
            action='store_true',
            help='Eliminar TODAS las sesiones, incluso las no expiradas',
        )

    def handle(self, *args, **options):
        if options['all']:
            # Eliminar todas las sesiones
            count = Session.objects.all().count()
            Session.objects.all().delete()
            self.stdout.write(
                self.style.SUCCESS(
                    f'Se eliminaron {count} sesiones (todas)'
                )
            )
        else:
            # Eliminar solo sesiones expiradas (comportamiento por defecto)
            count_before = Session.objects.all().count()
            Session.objects.filter(expire_date__lt=timezone.now()).delete()
            count_after = Session.objects.all().count()
            deleted = count_before - count_after
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Se eliminaron {deleted} sesiones expiradas'
                )
            )
            
            if count_after > 0:
                self.stdout.write(
                    self.style.WARNING(
                        f'Quedan {count_after} sesiones activas. '
                        'Usa --all para eliminar todas.'
                    )
                )
