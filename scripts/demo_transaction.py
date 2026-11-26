from app.infrastructure.database.models import PlayerModel, TeamModel
from app.infrastructure.database.session import SessionLocal


def main():
    db = SessionLocal()
    test_team_name = "Tranzaksiya Test FC"

    print("1. Bitta tranzaksiyada jamoa va noto'g'ri o'yinchi qo'shishga urinish...")
    try:
        new_team = TeamModel(name=test_team_name, city="Samarqand")
        db.add(new_team)
        db.flush()  # Bazaga vaqtinchalik yuborib, ID olamiz (hali commit qilinmagan)
        print(f"   Vaqtinchalik jamoa ID olindi: {new_team.id}")

        # Ikkinchi qadamda ataylab xatolik yuz beradi (masalan, raqam 1-99 oralig'idan tashqarida)
        invalid_jersey = 150
        if not (1 <= invalid_jersey <= 99):
            raise ValueError(f"Noto'g'ri futbolka raqami: {invalid_jersey}")

        db.add(PlayerModel(full_name="Test O'yinchi", team_id=new_team.id, jersey_number=invalid_jersey, position="Himoyachi"))
        db.commit()
    except ValueError as err:
        db.rollback()
        print(f"   Xatolik yuz berdi -> {err}")
        print("   Tranzaksiya bekor qilindi (ROLLBACK bajarildi).")

    # Bazada chala ma'lumot qolmaganini tekshiramiz
    exists = db.query(TeamModel).filter(TeamModel.name == test_team_name).first()
    print(f"2. Tekshiruv natijasi: '{test_team_name}' bazada bormi? -> {exists is not None}")
    db.close()


if __name__ == "__main__":
    main()