"""
# Flask - Python의 마이크로 웹 프레임워크로 웹 애플리케이션을 빠르게 개발할 수 있도록 도와주는 프레임워크
# Flask-Smorest - Flask에서 Swagger 문서와 함께 API 를 쉽게 작성할 수 있도록 도와주는 라이브러리
# Schemas (Mashmallow 기반) - BookSchema 를 사용하여 API 에서 주고받은 데이터의 유효성 검사를 진행 후 변환한다.
"""

from flask.views import MethodView  # MethodView : Flask의 클래스 기반 뷰를 사용하여 APi를 정의할 수 있도록 제공
from flask_smorest import Blueprint, abort # Blueprint : API의 라우팅(여러 API 엔드포인트를 그룹)을 관리하는 역할 / abort() : 특정 상황에서 오류 응답을 반환할 때 사용됨. (ex: 찾을 수 없는 데이터 요청 시 `404` 반환)
from schemas import BookSchema  # 요청 및 응답 데이터의 검증을 위한 Schema

# 
book_blp = Blueprint('books', 'books', url_prefix='/books', description='Operations on books')

books = [] # 책 데이터를 저장할 리스트 (임시 데이터 저장소)

@book_blp.route('/')
class BookList(MethodView):
    
    # 모든 책 데이터를 반환하는 API
    @book_blp.response(200, BookSchema(many=True)) # 여러 개의 책 데이터를 반환할 것임을 명시
    def get(self):
        return books

    @book_blp.arguments(BookSchema)
    @book_blp.response(201, BookSchema)
    def post(self, new_data):
        new_data['id'] = len(books) + 1 # 자동으로 ID 할당 (1부터 삽입))
        new_data['date'] = "25.02.25"
        books.append(new_data)
        print(books)
        return new_data

@book_blp.route('/<int:book_id>')
class Book(MethodView):
    @book_blp.response(200, BookSchema)
    def get(self, book_id):
        book = next((book for book in books if book['id'] == book_id), None)
        if book is None:
            abort(404, message="Book not found.")
        return book

    @book_blp.arguments(BookSchema)
    @book_blp.response(200, BookSchema)
    def put(self, new_data, book_id):
        book = next((book for book in books if book['id'] == book_id), None)
        if book is None:
            abort(404, message="Book not found.")
        book.update(new_data)
        return book

    @book_blp.response(204)
    def delete(self, book_id):
        global books
        book = next((book for book in books if book['id'] == book_id), None)
        if book is None:
            abort(404, message="Book not found.")
        books = [book for book in books if book['id'] != book_id]
        return ''