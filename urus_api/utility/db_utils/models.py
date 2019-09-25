from urus_api import db


def to_dict(self, filter_type=None, filter_columns=[]):
    d = {}
    for c in self.__table__.columns:
        if filter_type == "include":
            if str(c.name) in filter_columns:
                d[c.name] = getattr(self, c.name, None)
        elif filter_type == "exclude":
            if str(c.name) not in filter_columns:
                d[c.name] = getattr(self, c.name, None)
        else:
            d[c.name] = getattr(self, c.name, None)
    return d
    # return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}


db.Model.to_dict = to_dict


class BcLineBroadcast(db.Model):
    __tablename__ = 'bc_line_broadcast'

    line_id = db.Column(db.String(255, 'utf8_unicode_ci'), primary_key=True)
    broadcast = db.Column(
        db.ForeignKey('bc_line_broadcast_item.item_number'),
        primary_key=True,
        nullable=False,
        index=True)
    create_at = db.Column(db.DateTime)
    update_at = db.Column(db.DateTime)
    user_status = db.Column(db.String(1, 'utf8_unicode_ci'))
    source = db.Column(db.String(45, 'utf8_unicode_ci'))

    bc_line_broadcast_item = db.relationship('BcLineBroadcastItem')


class BcLineBroadcastCategory(db.Model):
    __tablename__ = 'bc_line_broadcast_category'

    category_number = db.Column(db.INTEGER, primary_key=True)
    category_name = db.Column(db.String(45, 'utf8_unicode_ci'))
    category_status = db.Column(db.String(1, 'utf8_unicode_ci'))
    category_content = db.Column(db.String(255, 'utf8_unicode_ci'))
    category_page = db.Column(db.INTEGER)


class BcLineBroadcastItem(db.Model):
    __tablename__ = 'bc_line_broadcast_item'

    item_number = db.Column(db.INTEGER, primary_key=True)
    item_name = db.Column(db.String(45, 'utf8_unicode_ci'))
    item_status = db.Column(db.String(1, 'utf8_unicode_ci'))
    item_content = db.Column(db.String(255, 'utf8_unicode_ci'))
    item_category = db.Column(
        db.ForeignKey('bc_line_broadcast_category.category_number'), index=True)

    item_customer_default = db.Column(db.String(1, 'utf8_unicode_ci'))
    bc_line_broadcast_category = db.relationship('BcLineBroadcastCategory')


class EcPfBotLineMember(db.Model):
    __tablename__ = 'ec_pf_bot_line_member'

    uuidpk = db.Column(db.String(255, 'utf8_unicode_ci'), primary_key=True)
    created_at = db.Column(db.DateTime)
    created_by = db.Column(db.String(255, 'utf8_unicode_ci'))
    cust_id = db.Column(db.String(255, 'utf8_unicode_ci'))
    modified_at = db.Column(db.DateTime)
    modified_by = db.Column(db.String(255, 'utf8_unicode_ci'))
    line_id = db.Column(db.String(255, 'utf8_unicode_ci'), unique=True)
    mem_id = db.Column(db.String(255, 'utf8_unicode_ci'))
    nick_name = db.Column(db.String(255, 'utf8_unicode_ci'))
    picture = db.Column(db.String(255, 'utf8_unicode_ci'))


class EcPfMemberD(db.Model):
    __tablename__ = 'ec_pf_member_d'

    uuidpk = db.Column(db.String(255, 'utf8_unicode_ci'), primary_key=True)
    created_at = db.Column(db.DateTime)
    created_by = db.Column(db.String(255, 'utf8_unicode_ci'))
    modified_at = db.Column(db.DateTime)
    modified_by = db.Column(db.String(255, 'utf8_unicode_ci'))
    inv = db.Column(db.String(255, 'utf8_unicode_ci'))
    invitation_code = db.Column(db.String(255, 'utf8_unicode_ci'))
    verify_email = db.Column(db.String(255, 'utf8_unicode_ci'))
    verify_fb = db.Column(db.String(255, 'utf8_unicode_ci'))
    verify_google = db.Column(db.String(255, 'utf8_unicode_ci'))
    verify_mobile = db.Column(db.String(255, 'utf8_unicode_ci'))
    verify_sinopac = db.Column(db.String(255, 'utf8_unicode_ci'))
    verify_sinopac_appreciation = db.Column(db.String(255, 'utf8_unicode_ci'))


class EcPfMember(db.Model):
    __tablename__ = 'ec_pf_member'

    uuidpk = db.Column(db.String(255, 'utf8_unicode_ci'), primary_key=True)
    created_at = db.Column(db.DateTime)
    created_by = db.Column(db.String(255, 'utf8_unicode_ci'))
    cust_id = db.Column(db.String(255, 'utf8_unicode_ci'))
    modified_at = db.Column(db.DateTime)
    modified_by = db.Column(db.String(255, 'utf8_unicode_ci'))
    bday = db.Column(db.String(255, 'utf8_unicode_ci'))
    career = db.Column(db.String(255, 'utf8_unicode_ci'))
    email = db.Column(db.String(255, 'utf8_unicode_ci'))
    first_name = db.Column(db.String(255, 'utf8_unicode_ci'))
    gender = db.Column(db.String(255, 'utf8_unicode_ci'))
    id_number = db.Column(db.String(255, 'utf8_unicode_ci'), unique=True)
    last_name = db.Column(db.String(255, 'utf8_unicode_ci'))
    locale = db.Column(db.String(255, 'utf8_unicode_ci'))
    middle_name = db.Column(db.String(255, 'utf8_unicode_ci'))
    mobile = db.Column(db.String(255, 'utf8_unicode_ci'))
    mem_name = db.Column(db.String(255, 'utf8_unicode_ci'))
    nick_name = db.Column(db.String(255, 'utf8_unicode_ci'))
    mem_pass = db.Column(db.String(255, 'utf8_unicode_ci'))
    pic = db.Column(db.String(255, 'utf8_unicode_ci'))  # db is LONGTEXT
    status = db.Column(db.String(255, 'utf8_unicode_ci'))
    timezone = db.Column(db.String(255, 'utf8_unicode_ci'))
    mem_type = db.Column(db.String(255, 'utf8_unicode_ci'))
    memd_id = db.Column(db.ForeignKey('ec_pf_member_d.uuidpk'), index=True)
    fb_bind_at = db.Column(db.DateTime)
    sino_bind_at = db.Column(db.DateTime)
    line_bind_at = db.Column(db.DateTime)
    last_login_at = db.Column(db.DateTime)
    accttype = db.Column(db.String(255, 'utf8_unicode_ci'))

    memd = db.relationship('EcPfMemberD')


# db.create_all()