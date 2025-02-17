set -o errexit

cd backend

pip install -r requirements.txt

python manage.py collectstatic --no-input

python manage.py migrate

if [[ $CREATE_SUPERUSER ]]; then
    python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'Felix3001')
"
fi