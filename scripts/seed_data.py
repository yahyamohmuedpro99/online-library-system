import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.services.book_service import BookService
from app.services.auth_service import AuthService
from scripts.mock_generators import MockDataGenerator
import click

def seed_users(count=20):
    """Seed users into the database"""
    print(f"Seeding {count} users...")
    users_data = MockDataGenerator.generate_user_data(count)
    
    created_count = 0
    for user_data in users_data:
        try:
            AuthService.signup(user_data)
            created_count += 1
        except Exception as e:
            print(f"Failed to create user {user_data['email']}: {str(e)}")
    
    print(f"Successfully created {created_count} users")
    return created_count

def seed_books(count=50, include_specific=True):
    """Seed books into the database"""
    books_created = 0
    
    # Add specific well-known books first
    if include_specific:
        print("Seeding specific well-known books...")
        specific_books = MockDataGenerator.generate_specific_books()
        
        for book_data in specific_books:
            try:
                BookService.create_book(book_data)
                books_created += 1
            except Exception as e:
                print(f"Failed to create book '{book_data['title']}': {str(e)}")
    
    # Add random generated books
    print(f"Seeding {count} random books...")
    books_data = MockDataGenerator.generate_book_data(count)
    
    for book_data in books_data:
        try:
            BookService.create_book(book_data)
            books_created += 1
        except Exception as e:
            print(f"Failed to create book '{book_data['title']}': {str(e)}")
    
    print(f"Successfully created {books_created} books")
    return books_created

def clear_all_data():
    """Clear all data from the database"""
    print("Clearing all data...")
    
    # Clear books
    db.session.execute(db.text("DELETE FROM book"))
    
    # Clear users
    db.session.execute(db.text("DELETE FROM user"))
    
    db.session.commit()
    print("All data cleared successfully")

@click.command()
@click.option('--users', default=20, help='Number of users to create')
@click.option('--books', default=50, help='Number of random books to create')
@click.option('--clear', is_flag=True, help='Clear all existing data first')
@click.option('--no-specific', is_flag=True, help='Skip creating specific well-known books')
def seed_database(users, books, clear, no_specific):
    """Seed the database with mock data"""
    app = create_app()
    
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
        if clear:
            clear_all_data()
        
        # Seed users
        users_created = seed_users(users)
        
        # Seed books
        books_created = seed_books(books, include_specific=not no_specific)
        
        print(f"\n✅ Database seeding completed!")
        print(f"📊 Summary:")
        print(f"   - Users created: {users_created}")
        print(f"   - Books created: {books_created}")
        print(f"   - Total records: {users_created + books_created}")

if __name__ == '__main__':
    seed_database()
