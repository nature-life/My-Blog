import random
from MyBlog.models import Admin, Category, Post, Comment
from MyBlog.extensions import db
from faker import Faker
from sqlalchemy.exc import IntegrityError

fake = Faker(locale="zh_CN")


def fake_admin():
    admin = Admin(
        username='839307813',
        blog_title="my blog",
        blog_sub_title='yo~yo~yo!',
        name='名剑风流',
        about="Welcome to my personal website what likes uses python to coding",
        is_admin=True,
        is_superadmin=True
    )
    admin.set_password('ohj.136269')
    admin.set_super('ohj.135159')
    db.session.add(admin)
    db.session.commit()
    super = Admin(
        username='123456',
        blog_title="my blog",
        blog_sub_title='yo~yo~yo!',
        name='名剑风流',
        about="Welcome to my personal website what likes uses python to coding",
        is_admin=True,
        is_superadmin=False
    )
    super.set_password('ohj.136269')
    super.set_super('ohj.135159')
    db.session.add(super)
    db.session.commit()
    user = Admin(
        username='123456789',
        blog_title="my blog",
        blog_sub_title='yo~yo~yo!',
        name='名剑风流',
        about="Welcome to my personal website what likes uses python to coding",
        is_admin=False,
        is_superadmin=False
    )
    user.set_password('ohj.136269')
    user.set_super('ohj.135159')
    db.session.add(user)
    db.session.commit()


def fake_category(count=5):
    # 定义默认分类
    category = Category(name='Default')
    db.session.add(category)

    for i in range(count):
        category = Category(name=fake.word())
        db.session.add(category)
        # 若随机生成分类名重复则回滚，取消添加到category的临时会话
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def fake_post(count=25):
    for i in range(count):
        post = Post(
            title=fake.sentence(),
            body=fake.text(2000),
            category=Category.query.get(random.randint(1, Category.query.count())),
            timestamp=fake.date_time_this_year(),
            admin=Admin.query.get(random.randint(1, Admin.query.count()))
        )
        db.session.add(post)
    db.session.commit()


def fake_comment(count=150):
    for i in range(count):
        comment = Comment(
            admin=Admin.query.get(random.randint(1, Admin.query.count())),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            post=Post.query.get(random.randint(1, Post.query.count())),
            reviewed=True
        )
        db.session.add(comment)
    db.session.commit()
    for i in range(count):
        comment = Comment(
            admin=Admin.query.get(random.randint(1, Admin.query.count())),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            post=Post.query.get(random.randint(1, Post.query.count())),
            replied=Comment.query.get(random.randint(1, Comment.query.count())),
            reviewed=True
        )
        db.session.add(comment)
