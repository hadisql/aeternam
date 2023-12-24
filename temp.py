from django.contrib.auth import get_user_model
from accounts.models import Relation


User = get_user_model()

# List of emails
emails = ['hadi@example.com','zousqa@gmail.com', 'wabperso@gmail.com', 'Dbouzoubaa@gmail.com',
          'bouzoubaa_zineb@hotmail.com', 'sqallim@yahoo.com', 'mounir.mikou@gmail.com',
          'nouzhabaya@gmail.com', 'samiasayarh@gmail.com']

# Common password for all users
password = 'changez-moi'

# Loop to create users
for email in emails:
    user, created = User.objects.get_or_create(email=email, defaults={'password': password})

    if created:
        print(f"User '{email}' created successfully.")
    else:
        print(f"User '{email}' already exists.")

for i, sender_email in enumerate(emails):
    sender = User.objects.get(email=sender_email)

    for receiver_email in emails:
        if sender_email != receiver_email:  # Avoid creating relation with oneself
            receiver = User.objects.get(email=receiver_email)

            # Check if the relation already exists
            if not Relation.objects.filter(user_sending=sender, user_receiving=receiver).exists():
                # Create a new relation
                relation = Relation(user_sending=sender, user_receiving=receiver, relation_type='UNDEFINED')
                relation.save()

print("Relations created successfully.")
