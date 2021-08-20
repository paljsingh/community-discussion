import json
from functools import partial
from http import HTTPStatus

from pymodm import MongoModel
from pymodm.files import File
from pymodm.fields import CharField, DateTimeField, ImageField, FileField
from pymongo.write_concern import WriteConcern

from random import Random

import uuid
import logging.config
from faker import Faker
from datetime import datetime
from common.customflask import CustomFlask
from common.customverifier import CustomJWTVerifier
from werkzeug.exceptions import HTTPException, abort
from flask import request

from common.db import Db
from common.utils import FlaskUtils
from kafka import KafkaProducer
import atexit

logging.config.fileConfig('../logging.conf')
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = CustomFlask(__name__)
app.config['MONGODB_SETTINGS'] = {'host': app.conf.get('db_uri')}
db = Db()
producer = KafkaProducer(bootstrap_servers=app.conf.get('kafka_endpoints'),
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

atexit.register(partial(FlaskUtils.graceful_shutdown, db=db, kafka_producer=producer))

for cls in HTTPException.__subclasses__():
    app.register_error_handler(cls, CustomJWTVerifier.handle_error)


@app.route("/api/v1/communities/<community_id>/posts/new", methods=['POST'])
@CustomJWTVerifier.verify_jwt_token
def create_new_post(community_id, my_id, is_admin=False):

    content = request.get_json()
    new_post = Post(created_by=my_id, content=content, community_id=community_id)
    new_post.save()

    # notify kafka about new post
    producer.send('communities', {'id': new_post.id, 'content': new_post.content, 'community_id': community_id,
                                  'user_id': my_id, 'creation_date': new_post.creation_date})
    return app.make_response(new_post.to_son())


@app.route("/api/v1/communities/<community_id>/images/new", methods=['POST'])
@CustomJWTVerifier.verify_jwt_token
def create_new_image_post(community_id, my_id, is_admin=False):
    allowed_ext = ['png', 'jpg', 'jpeg', 'gif']
    new_image_post = ImagePost(created_by=my_id, community_id=community_id)
    file = request.files['file']
    ext = file.filename.split('.')[1] if file.filename else None
    if ext in allowed_ext:
        new_image_post.file = File(file)
        new_image_post.save()

        producer.send('images', {'id': new_image_post.id, 'name': new_image_post.name, 'community_id': community_id,
                                 'user_id': my_id, 'creation_date': new_image_post.creation_date})

        return app.make_response(new_image_post.to_son())
    else:
        abort(HTTPStatus.PRECONDITION_FAILED)


@app.route("/api/v1/communities/<community_id>/videos/new", methods=['POST'])
@CustomJWTVerifier.verify_jwt_token
def create_new_video_post(community_id, my_id, is_admin=False):
    allowed_ext = ['.mp4', '.mkv', '.mov']
    new_video_post = VideoPost(created_by=my_id, community_id=community_id)
    file = request.files['file']
    ext = file.filename.split('.')[1] if file.filename else None

    if ext in allowed_ext:
        new_video_post.file = File(file)
        new_video_post.save()

        producer.send('videos', {'id': new_video_post.id, 'name': new_video_post.name, 'community_id': community_id,
                                 'user_id': my_id, 'creation_date': new_video_post.creation_date})

        return app.make_response(new_video_post.to_son())
    else:
        abort(HTTPStatus.PRECONDITION_FAILED)


@app.route("/api/v1/communities/<community_id>/posts", methods=['GET'])
@CustomJWTVerifier.verify_jwt_token
def get_all_posts(community_id, my_id, is_admin=False):
    posts = db.retrieve(Post, filters={'community_id': community_id})
    return app.make_response(posts)


@app.route("/api/v1/communities/<community_id>/images", methods=['GET'])
@CustomJWTVerifier.verify_jwt_token
def get_all_image_posts(community_id, my_id, is_admin=False):
    image_posts = db.retrieve(ImagePost, filters={'community_id': community_id})
    return app.make_response(image_posts)


@app.route("/api/v1/communities/<community_id>/videos", methods=['GET'])
@CustomJWTVerifier.verify_jwt_token
def get_all_video_posts(community_id, my_id, is_admin=False):
    video_posts = db.retrieve(VideoPost, filters={'community_id': community_id})
    return app.make_response(video_posts)


# TODO: Introduce private posts later.
@app.route('/api/v1/communities/<community_id>/posts/<post_id>', methods=['GET'])
@CustomJWTVerifier.verify_jwt_token
def get_post(community_id, post_id, my_id, is_admin=False):
    post = db.get(Post, post_id)
    return app.make_response(post.to_son())


@app.route('/api/v1/communities/<community_id>/images/<image_post_id>', methods=['GET'])
@CustomJWTVerifier.verify_jwt_token
def get_image_post(community_id, image_post_id, my_id, is_admin=False):
    image_post = db.get(ImagePost, image_post_id)
    return app.make_response(image_post.to_son())


@app.route('/api/v1/communities/<community_id>/videos/<video_post_id>', methods=['GET'])
@CustomJWTVerifier.verify_jwt_token
def get_video_post(community_id, video_post_id, my_id, is_admin=False):
    video_post = db.get(ImagePost, video_post_id)
    return app.make_response(video_post.to_son())


@app.route('/api/v1/communities/<community_id>/posts/search', methods=['GET'])
@CustomJWTVerifier.verify_jwt_token
def search_posts(community_id, my_id, is_admin=False):
    text, = FlaskUtils.get_url_args('text')

    # search for given name in indexed text-fields
    posts = db.retrieve(Post, {
        '$text': {
            '$search': text,
            '$caseSensitive': False,
            '$diacriticSensitive': False,   # treat é, ê the same as e
        }
    })

    # TODO: any history updates / events here.

    return app.make_response(posts)


# Usergroup related messages


@app.route("/api/v1/usergroups/<usergroup_id>/messages/new", methods=['POST'])
@CustomJWTVerifier.verify_jwt_token
def create_new_usergroup_post(usergroup_id, my_id, is_admin=False):

    content = request.get_json()
    new_post = Post(created_by=my_id, content=content, usergroup_id=usergroup_id)
    new_post.save()

    producer.send('posts', {'id': new_post.id, 'name': new_post.name, 'usergroup_id': usergroup_id,
                            'user_id': my_id, 'creation_date': new_post.creation_date})

    return app.make_response(new_post.to_son())


@app.route("/api/v1/usergroups/<usergroup_id>/images/new", methods=['POST'])
@CustomJWTVerifier.verify_jwt_token
def create_new_usergroup_image_post(usergroup_id, my_id, is_admin=False):
    allowed_ext = ['png', 'jpg', 'jpeg', 'gif']
    new_image_post = ImagePost(created_by=my_id, usergroup_id=usergroup_id)
    file = request.files['file']
    ext = file.filename.split('.')[1] if file.filename else None
    if ext in allowed_ext:
        new_image_post.file = File(file)
        new_image_post.save()

        producer.send('images', {'id': new_image_post.id, 'name': new_image_post.name, 'usergroup_id': usergroup_id,
                                 'user_id': my_id, 'creation_date': new_image_post.creation_date})

        return app.make_response(new_image_post.to_son())
    else:
        abort(HTTPStatus.PRECONDITION_FAILED)


@app.route("/api/v1/usergroups/<usergroup_id>/videos/new", methods=['POST'])
@CustomJWTVerifier.verify_jwt_token
def create_new_usergroup_video_post(usergroup_id, my_id, is_admin=False):
    allowed_ext = ['.mp4', '.mkv', '.mov']
    new_video_post = VideoPost(created_by=my_id, usergroup_id=usergroup_id)
    file = request.files['file']
    ext = file.filename.split('.')[1] if file.filename else None

    if ext in allowed_ext:
        new_video_post.file = File(file)
        new_video_post.save()

        producer.send('videos', {'id': new_video_post.id, 'name': new_video_post.name, 'usergroup_id': usergroup_id,
                                 'user_id': my_id, 'creation_date': new_video_post.creation_date})

        return app.make_response(new_video_post.to_son())
    else:
        abort(HTTPStatus.PRECONDITION_FAILED)


@app.route("/api/v1/usergroups/<usergroup_id>/messages", methods=['GET'])
@CustomJWTVerifier.verify_jwt_token
def get_all_usergroup_posts(usergroup_id, my_id, is_admin=False):
    print("I am called")
    posts = db.retrieve(Post, filters={'usergroup_id': usergroup_id})
    print(posts)
    return app.make_response(posts)


@app.route("/api/v1/usergroups/<usergroup_id>/images", methods=['GET'])
@CustomJWTVerifier.verify_jwt_token
def get_all_usergroup_image_posts(usergroup_id, my_id, is_admin=False):
    image_posts = db.retrieve(ImagePost, filters={'usergroup_id': usergroup_id})
    return app.make_response(image_posts)


@app.route("/api/v1/usergroups/<usergroup_id>/videos", methods=['GET'])
@CustomJWTVerifier.verify_jwt_token
def get_all_usergroup_video_posts(usergroup_id, my_id, is_admin=False):
    video_posts = db.retrieve(VideoPost, filters={'usergroup_id': usergroup_id})
    return app.make_response(video_posts)


# TODO: Introduce private posts later.
@app.route('/api/v1/usergroups/<usergroup_id>/messages/<message_id>', methods=['GET'])
@CustomJWTVerifier.verify_jwt_token
def get_usergroup_post(usergroup_id, message_id, my_id, is_admin=False):
    print("I am called with message id")
    post = db.get(Post, message_id)
    return app.make_response(post.to_son())


@app.route('/api/v1/usergroups/<usergroup_id>/images/<image_id>', methods=['GET'])
@CustomJWTVerifier.verify_jwt_token
def get_usergroup_image_post(usergroup_id, image_id, my_id, is_admin=False):
    image_post = db.get(ImagePost, image_id)
    return app.make_response(image_post.to_son())


@app.route('/api/v1/usergroups/<usergroup_id>/videos/<video_id>', methods=['GET'])
@CustomJWTVerifier.verify_jwt_token
def get_usergroup_video_post(usergroup_id, video_id, my_id, is_admin=False):
    video_post = db.get(ImagePost, video_id)
    return app.make_response(video_post.to_son())


@app.route('/api/v1/usergroups/<usergroup_id>/messages/search', methods=['GET'])
@CustomJWTVerifier.verify_jwt_token
def search_usergroup_posts(usergroup_id, my_id, is_admin=False):
    text, = FlaskUtils.get_url_args('text')

    # search for given name in indexed text-fields
    posts = db.retrieve(Post, {
        '$text': {
            '$search': text,
            '$caseSensitive': False,
            '$diacriticSensitive': False,   # treat é, ê the same as e
        }
    })

    # TODO: any history updates / events here.

    return app.make_response(posts)


# TODO
# api to update community info.
# api for invite status check.


class Post(MongoModel):
    """
    For now, using Post object for both usergroup/user chat messages and the community posts.
    A distinction may be made later.
    """
    id = CharField(required=True, primary_key=True, default=uuid.uuid4)
    content = CharField(required=True)
    created_by = CharField(required=True)
    community_id = CharField(required=True)
    usergroup_id = CharField(required=True)
    creation_date = DateTimeField(required=True, default=datetime.utcnow)

    def fake_info(self):
        self.content = Faker().paragraph(nb_sentences=Random().randint(20, 50))

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'my-app'


class ImagePost(Post):
    file = ImageField(required=True)

    # TODO: move the fake image generation to an external tool.
    # def fake_info(self):
    #     r = Random()
    #     f = Faker()
    #     self.file = Image.new('RGB', (100, 100), color=(r.randint(1, 255), r.randint(1, 255), r.randint(1, 255)))
    #     self.file.save('{}.png'.format(f.word()))

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'my-app'


class VideoPost(Post):
    file = FileField(required=True)

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'my-app'
