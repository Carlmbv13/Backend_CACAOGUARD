from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from farms.models import Farm
from scans.models import Scan
from alerts.models import Alert
from decimal import Decimal
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Seed database with initial test data'
    
    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')
        
        # Clear existing data (optional)
        self.stdout.write('Clearing existing data...')
        Alert.objects.all().delete()
        Scan.objects.all().delete()
        Farm.objects.all().delete()
        User.objects.exclude(is_superuser=True).delete()
        
        # Create admin user
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@cacaoguard.com',
            password='admin123',
            first_name='Admin',
            last_name='User'
        )
        admin.profile.role = 'Admin'
        admin.profile.save()
        self.stdout.write(f'✓ Created admin user: admin/admin123')
        
        # Create farmers
        farmer1 = User.objects.create_user(
            username='john_farmer',
            email='john@example.com',
            password='farmer123',
            first_name='John',
            last_name='Smith'
        )
        farmer1.profile.role = 'Farmer'
        farmer1.profile.phone = '+1234567890'
        farmer1.profile.save()
        
        farmer2 = User.objects.create_user(
            username='maria_farmer',
            email='maria@example.com',
            password='farmer123',
            first_name='Maria',
            last_name='Garcia'
        )
        farmer2.profile.role = 'Farmer'
        farmer2.profile.phone = '+1234567891'
        farmer2.profile.save()
        
        self.stdout.write('✓ Created farmer users')
        
        # Create technician
        tech = User.objects.create_user(
            username='tech_support',
            email='tech@cacaoguard.com',
            password='tech123',
            first_name='Support',
            last_name='Technician'
        )
        tech.profile.role = 'Technician'
        tech.profile.save()
        self.stdout.write('✓ Created technician user')
        
        # Create farms for farmer1
        farm1 = Farm.objects.create(
            name='Green Valley Plantation',
            owner=farmer1,
            location='North Region, Plot 42',
            size_hectares=Decimal('35.50'),
            health_score=85.0,
            risk_level='Low'
        )
        
        farm2 = Farm.objects.create(
            name='Sunrise Estate',
            owner=farmer1,
            location='East Region, Plot 15',
            size_hectares=Decimal('28.75'),
            health_score=92.0,
            risk_level='Low'
        )
        
        # Create farms for farmer2
        farm3 = Farm.objects.create(
            name='River Side Farm',
            owner=farmer2,
            location='South Region, Plot 8',
            size_hectares=Decimal('42.00'),
            health_score=45.0,
            risk_level='High'
        )
        
        farm4 = Farm.objects.create(
            name='Mountain View Estate',
            owner=farmer2,
            location='West Region, Plot 23',
            size_hectares=Decimal('55.25'),
            health_score=30.0,
            risk_level='Critical'
        )
        
        self.stdout.write('✓ Created 4 farms')
        
        # Create scans for farm1 (healthy)
        Scan.objects.create(
            farm=farm1,
            zone_name='Zone A - North',
            severity='Healthy',
            confidence=98.5,
            affected_area=Decimal('0.00'),
            date=datetime.now() - timedelta(days=2)
        )
        
        Scan.objects.create(
            farm=farm1,
            zone_name='Zone B - East',
            severity='Mild',
            confidence=87.3,
            affected_area=Decimal('5.50'),
            date=datetime.now() - timedelta(days=1)
        )
        
        # Create scans for farm3 (moderate to severe)
        scan_severe = Scan.objects.create(
            farm=farm3,
            zone_name='Zone C - South',
            severity='Moderate',
            confidence=91.2,
            affected_area=Decimal('12.75'),
            date=datetime.now() - timedelta(hours=12)
        )
        
        # This will automatically create an alert
        scan_critical = Scan.objects.create(
            farm=farm4,
            zone_name='Zone D - West',
            severity='Severe',
            confidence=94.8,
            affected_area=Decimal('28.50'),
            date=datetime.now() - timedelta(hours=6)
        )
        
        # Create additional alerts manually
        Alert.objects.create(
            farm=farm3,
            severity='warning',
            message='Moderate Black Pod Disease detected in Zone C. Monitoring recommended.',
            status='new'
        )
        
        Alert.objects.create(
            farm=farm4,
            severity='critical',
            message='CRITICAL: Severe outbreak in Zone D. Immediate treatment required!',
            status='new'
        )
        
        Alert.objects.create(
            farm=farm1,
            severity='info',
            message='Routine scan completed. Farm health status: Good.',
            status='acknowledged'
        )
        
        self.stdout.write('✓ Created scans and alerts')
        
        # Update farm health scores based on scans
        farm3.health_score = 45.0
        farm3.risk_level = 'High'
        farm3.save()
        
        farm4.health_score = 30.0
        farm4.risk_level = 'Critical'
        farm4.save()
        
        self.stdout.write(self.style.SUCCESS('✓ Database seeding completed successfully!'))
        self.stdout.write('\nTest Credentials:')
        self.stdout.write('Admin: admin / admin123')
        self.stdout.write('Farmer1: john_farmer / farmer123')
        self.stdout.write('Farmer2: maria_farmer / farmer123')
        self.stdout.write('Technician: tech_support / tech123')