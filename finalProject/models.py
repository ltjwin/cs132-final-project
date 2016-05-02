from finalProject import db

class Warning(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	county = db.Column(db.String(100))
	warning_type = db.Column(db.String(100))
	station = db.Column(db.String(100))
	date = db.Column(db.DateTime);
	warning_exists =  db.Column(db.Boolean)
