from __future__ import print_function
from imgurpython import ImgurClient
from imgurpython.helpers.error import ImgurClientError
from PIL import Image
from numpy import unique

import os
import sys
import urllib
import io
import hashlib
import collections

client = ImgurClient(os.environ['IMGUR_CLIENT_ID'], os.environ['IMGUR_CLIENT_SECRET'], os.environ['IMGUR_ACCESS_TOKEN'], os.environ['IMGUR_REFRESH_TOKEN'])

album_id = raw_input('Album Id: ')

print('OK, first I need to download all images in this album.')
album_images = client.get_album_images(album_id)
image_md5_link_lookups = []

for counter, image in enumerate(album_images):
    image_handle = urllib.urlopen(image.link)
    image_data = image_handle.read()

    md5 = hashlib.md5()
    md5.update(image_data)
    digest = md5.hexdigest()

    image_md5_link_lookups.append({'id': image.id, 'digest': digest})

    print('Downloaded {}/{} images'.format(counter, len(album_images)), end='\r')
    sys.stdout.flush()

print('Done. Removing all duplicate images now...')

only_digests = list(map(lambda image: image['digest'], image_md5_link_lookups))
counter = collections.Counter(only_digests)
duplicate_digests = [i for i in counter if counter[i]>1]

ids = []
for digest in duplicate_digests:
    duplicate_images_ids = [str(lu['id']) for lu in image_md5_link_lookups if lu['digest'] == digest]
    ids.extend(duplicate_images_ids[1:])

for id in ids:
    client.delete_image(id)

print('Done. Deleted {} images.'.format(len(ids)))


