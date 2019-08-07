import time
from uuid import uuid1
from create_tables import session, User, WeiBoContent
from get_weibo_content import read_ids, get_user_info, get_weibo


for id in read_ids('id.txt'):
    info = get_user_info(id)
    if info is not None:
        user = User(
                user_id = uuid1().hex,
                weibo_id = id,
                screen_name = info[0],
                profile_url = info[1],
                profile_image_url = info[2],
                verified = info[3],
                description = info[4],
                follow_count = info[5],
                followers_count = info[6],
                gender = info[7],
                urank = info[8]
            )
        try:
            session.add(user)
            session.commit()
        except Exception as e:
            session.rollback()
            print(e)
            continue
    print('\n'*3)
    time.sleep(3)
    
for id in read_ids('id.txt'):
    contents = get_weibo(id)
    if len(contents) != 0:
        for content in contents:
            cont = WeiBoContent(
                    content_id = uuid1().hex,
                    weibo_id = id,
                    created_at = content[0],
                    attitudes_count = content[1],
                    comments_count = content[2],
                    reposts_count = content[3],
                    scheme = content[4],
                    text = content[5]
                )
            try:
                session.add(cont)
                session.commit()
            except Exception as e:
                session.rollback()
                print(e)
                continue
    time.sleep(3)




