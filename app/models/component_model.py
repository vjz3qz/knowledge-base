from database_service import db



class Component(db.Model):
    id = db.Column(db.BIGINT, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.TEXT, nullable=False)
    location = db.Column(db.TEXT, nullable=False)    
    media = db.relationship('Media', secondary=media_component_association, back_populates="components")
    text_search_vector = db.Column(db.TSVECTOR)

    def __repr__(self):
        return f'<Component {self.id}>'

