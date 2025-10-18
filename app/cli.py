from __future__ import annotations
from flask import Flask
from .extensions import db
from .models import User, Interest, Skill


def register_cli(app: Flask) -> None:
    @app.cli.command("seed")
    def seed():
        # Minimal Kenyan-flavored seed data
        interests = ["Tech", "Business", "Gengetone", "Comedy", "Football", "Agriculture"]
        skills = ["Python", "Design", "Marketing", "Photography", "Farming"]
        for name in interests:
            if not db.session.execute(db.select(Interest).filter_by(name=name)).scalar():
                db.session.add(Interest(name=name))
        for name in skills:
            if not db.session.execute(db.select(Skill).filter_by(name=name)).scalar():
                db.session.add(Skill(name=name))
        if not db.session.execute(db.select(User).filter_by(email="demo@chooza.ke")).scalar():
            u = User(email="demo@chooza.ke", name="Demo User", county="Nairobi")
            u.set_password("password")
            db.session.add(u)
        db.session.commit()
        print("Seeded demo data.")
