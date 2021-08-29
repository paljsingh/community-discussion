import json
import os
import sys
from functools import partial
from http import HTTPStatus

from pymodm import MongoModel
from pymodm.files import File
from pymodm.fields import CharField, DateTimeField
from pymongo.write_concern import WriteConcern

import uuid
import logging.config
from datetime import datetime
from common.customflask import CustomFlask
from common.customverifier import CustomJWTVerifier
from werkzeug.exceptions import HTTPException, abort
from flask import request

from common.db import Db
from common.utils import FlaskUtils
from kafka import KafkaProducer
import atexit
from flask import send_file

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

data_dir = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "../../data")
images_dir = os.path.join(data_dir, app.conf.get('images_dir'))
videos_dir = os.path.join(data_dir, app.conf.get('videos_dir'))


@app.route("/api/v1/communities/<community_id>/posts/new", methods=['POST'])
@CustomJWTVerifier.verify_jwt_token
def create_new_post(community_id, my_id, is_admin=False):

    json_content = request.get_json()
    if not json_content and not json_content.get('content'):
        abort(HTTPStatus.PRECONDITION_FAILED)

    text_content = json_content['content']
    new_post = TextPost(created_by=my_id, content=text_content, community_id=community_id)
    new_post.save()

    # notify kafka about new post
    producer.send('posts', '{id},{community_id},{usergroup_id},{created_by},{content},{creation_date},{action}'.format(
        id=new_post.id, community_id=community_id, usergroup_id='', created_by=my_id, content=new_post.content,
        creation_date=new_post.creation_date.isoformat(), action='new post'))
    return app.make_response(new_post.to_son())


@app.route("/api/v1/communities/<community_id>/images/new", methods=['POST'])
@CustomJWTVerifier.verify_jwt_token
def create_new_image_post(community_id, my_id, is_admin=False):
    allowed_ext = ['png', 'jpg', 'jpeg', 'gif']
    filename = json.loads(request.form['json'])['name']

    if not filename:
        abort(HTTPStatus.PRECONDITION_FAILED)

    ext = filename.split('.')[1] if filename else None

    if ext not in allowed_ext:
        abort(HTTPStatus.PRECONDITION_FAILED)

    image_id = uuid.uuid4()
    filepath = os.path.join(images_dir, str(image_id))
    file_content = request.files['content']
    file_content.save(filepath)

    new_image_post = ImagePost(id=image_id, created_by=my_id, community_id=community_id)
    new_image_post.name = filename
    new_image_post.save()

    # new_image_post.file = file_content
    producer.send('images',
                  '{id},{community_id},{usergroup_id},{created_by},{name},{creation_date},{action}'.format(
                    id=new_image_post.id, community_id=community_id, usergroup_id='', created_by=my_id,
                    name=new_image_post.name, creation_date=new_image_post.creation_date.isoformat(),
                    action='new image')
                  )

    return app.make_response(json.dumps(
        {'_id': new_image_post.id, 'name': new_image_post.name}))


@app.route("/api/v1/communities/<community_id>/videos/new", methods=['POST'])
@CustomJWTVerifier.verify_jwt_token
def create_new_video_post(community_id, my_id, is_admin=False):
    allowed_ext = ['mp4', 'mkv', 'mov']
    filename = json.loads(request.form['json'])['name']

    if not filename:
        abort(HTTPStatus.PRECONDITION_FAILED)

    ext = filename.split('.')[1] if filename else None

    if ext not in allowed_ext:
        abort(HTTPStatus.PRECONDITION_FAILED)

    video_id = uuid.uuid4()
    filepath = os.path.join(videos_dir, str(video_id))
    file_content = request.files['content']
    file_content.save(filepath)

    new_video_post = VideoPost(id=video_id, created_by=my_id, community_id=community_id)
    new_video_post.name = filename
    new_video_post.save()
    producer.send('videos', '{id},{community_id},{usergroup_id},{user_id},{name},{creation_date},{action}'.format(
        id=new_video_post.id, community_id=community_id, usergroup_id='', user_id=my_id, name=new_video_post.name,
        creation_date=new_video_post.creation_date.isoformat(), action='new video'))

    return app.make_response(json.dumps(
        {'_id': new_video_post.id, 'name': new_video_post.name}))


@app.route("/api/v1/communities/<community_id>/posts", methods=['GET'])
@CustomJWTVerifier.verify_jwt_token
def get_all_posts(community_id, my_id, is_admin=False):
    posts = db.retrieve(TextPost, filters={'community_id': community_id})
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
    post = db.get(TextPost, post_id)
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
    posts = db.retrieve(TextPost, {
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
    new_post = TextPost(created_by=my_id, content=content, usergroup_id=usergroup_id)
    new_post.save()

    producer.send('posts', '{id},{community_id},{usergroup_id},{created_by},{content},{creation_date},{action}'.format(
        id=new_post.id, community_id='', usergroup_id=usergroup_id, created_by=my_id, content=new_post.content,
        creation_date=new_post.creation_date.isoformat(), action='new message'))

    return app.make_response(new_post.to_son())


@app.route("/api/v1/usergroups/<usergroup_id>/images/new", methods=['POST'])
@CustomJWTVerifier.verify_jwt_token
def create_new_usergroup_image_post(usergroup_id, my_id, is_admin=False):
    allowed_ext = ['png', 'jpg', 'jpeg', 'gif']
    data = request.get_json()

    new_image_post = ImagePost(created_by=my_id, usergroup_id=usergroup_id)
    if data.get('name'):
        new_image_post.name = data['name']

    file = request.files['file']
    ext = file.filename.split('.')[1] if file.filename else None
    if ext in allowed_ext:
        new_image_post.file = File(file)
        new_image_post.save()

        producer.send('images',
                      '{id},{community_id},{usergroup_id},{created_by},{name},{creation_date},{action}'.format(
                          id=new_image_post.id, community_id='', usergroup_id=usergroup_id, created_by=my_id,
                          name=new_image_post.name, creation_date=new_image_post.creation_date.isoformat(),
                          action='new image')
                      )

        return app.make_response(new_image_post.to_son())
    else:
        abort(HTTPStatus.PRECONDITION_FAILED)


@app.route("/api/v1/usergroups/<usergroup_id>/videos/new", methods=['POST'])
@CustomJWTVerifier.verify_jwt_token
def create_new_usergroup_video_post(usergroup_id, my_id, is_admin=False):
    allowed_ext = ['.mp4', '.mkv', '.mov']
    data = request.get_json()

    new_video_post = VideoPost(created_by=my_id, usergroup_id=usergroup_id)

    if data.get('name'):
        new_video_post.name = data['name']

    file = request.files['file']
    ext = file.filename.split('.')[1] if file.filename else None

    if ext in allowed_ext:
        new_video_post.file = File(file)
        new_video_post.save()

        producer.send('videos', '{id},{community_id},{usergroup_id},{user_id},{name},{creation_date},{action}'.format(
            id=new_video_post.id, community_id='', usergroup_id=usergroup_id, user_id=my_id, name=new_video_post.name,
            creation_date=new_video_post.creation_date.isoformat(), action='new video'))

        return app.make_response(new_video_post.to_son())
    else:
        abort(HTTPStatus.PRECONDITION_FAILED)


@app.route("/api/v1/usergroups/<usergroup_id>/messages", methods=['GET'])
@CustomJWTVerifier.verify_jwt_token
def get_all_usergroup_posts(usergroup_id, my_id, is_admin=False):
    posts = db.retrieve(TextPost, filters={'usergroup_id': usergroup_id})
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
    post = db.get(TextPost, message_id)
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
    posts = db.retrieve(TextPost, {
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


@app.route('/api/v1/image/<image_id>', methods=['GET'])
def get_image_file(image_id):
    img = db.get(ImagePost, image_id, to_son=False)
    filepath = os.path.join(images_dir, image_id)
    return send_file(filepath, download_name=img.name)


@app.route('/api/v1/video/<video_id>', methods=['GET'])
def get_video_file(video_id):
    vid = db.get(VideoPost, video_id, to_son=False)
    filepath = os.path.join(videos_dir, video_id)
    return send_file(filepath, download_name=vid.name)


class Post(MongoModel):
    """
    For now, using Post object for both usergroup/user chat messages and the community posts.
    A distinction may be made later.
    """
    id = CharField(required=True, primary_key=True, default=uuid.uuid4)
    created_by = CharField(required=True)
    community_id = CharField(required=True)
    usergroup_id = CharField(required=False)
    creation_date = DateTimeField(required=True, default=datetime.utcnow)

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'my-app'


class TextPost(Post):
    content = CharField(required=True)
    name = CharField(required=False)

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'my-app'


class ImagePost(Post):
    # file = FileField(required=True)
    name = CharField(required=False, blank=True)

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'my-app'


class VideoPost(Post):
    # file = FileField(required=True)
    name = CharField(required=False, blank=True)

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'my-app'
