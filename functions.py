def add_tags():
    all_tags = db.session.query(Tag.tag_name).all()
    all_tags_list = [v for v, in all_tags]

    for tag in all_tags_list:
        try:
            new_tag = request.form[tag]
            tag_used = Tag.query.filter(Tag.tag_name == new_tag).all()            

            link_tag = PostTag(post_id=id, tag_id=tag_used[0].id)

            db.session.add(link_tag)
            db.session.commit()
        except:
            pass