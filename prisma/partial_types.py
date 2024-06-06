from prisma.models import User

User.create_partial(name="UserSubFields", include={"id", "user_id", "name", "user_type"})