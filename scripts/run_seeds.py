#!/usr/bin/env python3
"""
Simple script runner for database seeding operations
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from scripts.seed_data import seed_users, seed_books, clear_all_data

def main():
    """Main function to run seeding operations"""
    app = create_app()
    
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
        print("🌱 Online Library System - Database Seeding")
        print("=" * 50)
        
        while True:
            print("\nChoose an option:")
            print("1. Seed everything (clear + users + books)")
            print("2. Seed users only")
            print("3. Seed books only")
            print("4. Clear all data")
            print("5. Quick seed (10 users + 20 books)")
            print("6. Large seed (50 users + 100 books)")
            print("0. Exit")
            
            choice = input("\nEnter your choice (0-6): ").strip()
            
            if choice == '0':
                print("👋 Goodbye!")
                break
            elif choice == '1':
                print("\n🧹 Clearing existing data...")
                clear_all_data()
                print("\n👥 Seeding users...")
                seed_users(20)
                print("\n📚 Seeding books...")
                seed_books(50, include_specific=True)
                print("\n✅ Complete seeding finished!")
                
            elif choice == '2':
                count = input("Number of users to create (default 20): ").strip()
                count = int(count) if count.isdigit() else 20
                seed_users(count)
                
            elif choice == '3':
                count = input("Number of books to create (default 50): ").strip()
                count = int(count) if count.isdigit() else 50
                include_specific = input("Include specific well-known books? (y/n, default y): ").strip().lower()
                include_specific = include_specific != 'n'
                seed_books(count, include_specific=include_specific)
                
            elif choice == '4':
                confirm = input("⚠️  Are you sure you want to clear ALL data? (yes/no): ").strip().lower()
                if confirm == 'yes':
                    clear_all_data()
                else:
                    print("❌ Operation cancelled")
                    
            elif choice == '5':
                print("\n🚀 Quick seeding...")
                seed_users(10)
                seed_books(20, include_specific=True)
                print("\n✅ Quick seeding completed!")
                
            elif choice == '6':
                print("\n🚀 Large seeding...")
                seed_users(50)
                seed_books(100, include_specific=True)
                print("\n✅ Large seeding completed!")
                
            else:
                print("❌ Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
