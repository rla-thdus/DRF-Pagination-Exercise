# Pagination
- [PageNumberPagination](#pagenumberpagination)
- [LimitOffsetPagination](#limitoffsetpagination)
- [CursorPagination](#cursorpagination)
- [언제 어떤 페이지네이션을 사용해야 할까](#그럼-언제-어떤-pagination을-사용해야-할까)

한정된 네트워크 자원을 효율적으로 사용하기 위해 데이터를 분할하여 DB에서 가져오는 방법을 의미한다.
대용량인 데이터를 요청할 때, 서버에서 모든 데이터를 한 번에 전달하면, 네트워크 통신에 있어 큰 비용이 발생한다.
이 때, 페이지네이션을 사용해서 한 번에 다 보내는 방식이 아닌 원하는 개수만큼 보내고, 다음에 똑같은 개수의 데이터를 추가로 보내줌으로써 데이터를 분할하여 전달한다.

## PageNumberPagination
전역에 `PageNumberPagination` 페이지네이션을 적용하기 위해서 프로젝트 settings.py에 아래의 코드를 추가해주면 된다.

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS' : 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE' : 2, # 한 페이지에 보여줄 데이터 개수를 뜻한다.
    ...
}
```

전역이 아닌 특정 View 별로 사용하고 싶다면 아래의 코드처럼 하면 된다.

```python
# PageNumberPagination을 상속받는 커스텀 페이지네이션을 만든다.
class PostPageNumberPagination(PageNumberPagination):
    page_size = 3 # 한 페이지에 보여줄 데이터 개수를 뜻한다. 
                  # page_size를 명시하지 않으면 settings에서 설정한 PAGE_SIZE를 따르고, 만약 명시되어 있지 않다면 전체 데이터를 반환한다.

# 페이지네이션을 사용할 뷰에 등록해준다.
class PostPageListAPIView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    pagination_class = PostPageNumberPagination
```

PageNumber pagination을 사용했을 때 날아가는 쿼리는 다음과 같다.
```SQL
SELECT 
    "api_post"."id",
    "api_post"."category_id",
    "api_post"."title",
    "api_post"."description",
    "api_post"."image",
    "api_post"."content",
    "api_post"."create_dt",
    "api_post"."update_dt",
    "api_post"."like"
FROM "api_post"
ORDER BY "api_post"."update_dt" ASC
LIMIT 3 OFFSET 3;
```

### 장점
- 유저가 페이지를 선택하고, 이동할 수 있다.
- 전체 페이지 수를 알 수 있다.

### 단점
- offset 위치를 계산하고, 필요한 데이터를 찾을 때까지 테이블을 풀 스캔한다.
- offset이 클수록 데이터베이스의 부하는 커진다.
- 다른 페이지로 넘어가는 과정에서 데이터의 CRUD가 발생했을 때 중복으로 노출되는 데이터가 있을 수도 있고 누락되는 데이터가 발생할 수 있다.

## LimitOffsetPagination
전역에 `LimitOffsetPagination` 페이지네이션을 적용하기 위해서 프로젝트 settings.py에 아래의 코드를 추가해주면 된다.
```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE' : 2, # 한 페이지에 보여줄 데이터 개수를 뜻한다.
    ...
}
```

전역이 아닌 특정 View 별로 사용하고 싶다면 아래의 코드처럼 하면 된다.

```python
# LimitOffsetPagination을 상속받는 커스텀 페이지네이션을 만든다.
class PostLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 3 # 한 페이지에 보여줄 데이터 개수를 뜻한다. 
                  # default_limit를 명시하지 않으면 settings에서 설정한 PAGE_SIZE를 따르고, 만약 명시되어 있지 않다면 전체 데이터를 반환한다.

# 페이지네이션을 사용할 뷰에 등록해준다.
class PostLimitListAPIView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    pagination_class = PostLimitOffsetPagination
```

LimitOffset pagination을 사용했을 때 날아가는 쿼리는 다음과 같다.
```SQL
SELECT
    "api_post"."id",
    "api_post"."category_id",
    "api_post"."title",
    "api_post"."description",
    "api_post"."image",
    "api_post"."content",
    "api_post"."create_dt",
    "api_post"."update_dt",
    "api_post"."like"
FROM "api_post"
ORDER BY "api_post"."update_dt" ASC
LIMIT 4 OFFSET 4;
```

### 장점
- 유저가 페이지를 선택하고, 이동할 수 있다.
- 전체 페이지 수를 알 수 있다.

### 단점
- offset 위치를 계산하고, 필요한 데이터를 찾을 때까지 테이블을 풀 스캔한다.
- offset이 클수록 데이터베이스의 부하는 커진다.
- 다른 페이지로 넘어가는 과정에서 데이터의 CRUD가 발생했을 때 중복으로 노출되는 데이터가 있을 수도 있고 누락되는 데이터가 발생할 수 있다.

## CursorPagination
ordering 기준으로 페이지는 구하는 방식을 말한다. 인덱스가 적용된 값을 비교하기에 테이블을 풀 스캔하지 않는다.
쿼리 파라미터로 `cursor` 값을 가지고 있는데 해당 값은 `offset=offset, reverse=reverse, position=position`을 encode 시킨 값이다.

전역에 `CursorPagination` 페이지네이션을 적용하기 위해서 프로젝트 settings.py에 아래의 코드를 추가해주면 된다.

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.CursorPagination',
    'PAGE_SIZE': 2 # 한 페이지에 보여줄 데이터 개수를 뜻한다.
}
```

전역이 아닌 특정 View 별로 사용하고 싶다면 아래의 코드처럼 하면 된다.

```python
# CursorPagination을 상속받는 커스텀 페이지네이션을 만든다.
class PostCursorPaginationPagination(CursorPagination):
    page_size = 3 # 한 페이지에 보여줄 데이터 개수를 뜻한다. 
                  # page_size를 명시하지 않으면 settings에서 설정한 PAGE_SIZE를 따르고, 만약 명시되어 있지 않다면 전체 데이터를 반환한다.
    ordering = 'order column' # 정렬 기준 컬럼이다. default는 -created 컬럼을 기준으로 한다. 컬럼명 앞에 "-"가 붙으면 내림 차순이다.

# 페이지네이션을 사용할 뷰에 등록해준다.
class PostCursorListAPIView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    pagination_class = PostCursorPaginationPagination
```

Cursor pagination을 사용할 때 날아가는 쿼리는 다음과 같다. ordering을 id로 해서 `where` 절을 보면 id로 조건을 주는 걸 확인할 수 있다.
```SQL
SELECT
    "api_post"."id",
    "api_post"."category_id",
    "api_post"."title",
    "api_post"."description",
    "api_post"."image",
    "api_post"."content",
    "api_post"."create_dt",
    "api_post"."update_dt",
    "api_post"."like"
FROM "api_post"
WHERE "api_post"."id" > 10
ORDER BY "api_post"."id" ASC
LIMIT 6;
```

### 장점
- 인덱스가 적용된 값을 비교하기 때문에 테이블을 풀 스캔하지 않는다.
- 데이터 CRUD가 빈번한 테이블이여도 다음 페이지 조회 시 값이 누락되지 않는다.

### 단점
- 전체 페이지 수를 알 수 없다.
- 정렬하는 값이 중복이 많은 경우 cursor pagination은 limit offset보다 느릴 수 있다.
  - 예를 들어 성으로 정렬을 했을 때 김씨인 사람이 여러 명이면 정상적으로 동작하지 않을 수 있다. 따라서 정렬을 추가로 더 해줘야 하는데 이렇게 되면 구현이 복잡해질 수 있다.

## 그럼 언제 어떤 Pagination을 사용해야 할까?
각각의 페이지네이션은 장단점을 가지고 있다. 실시간 서비스고 대량의 데이터가 빈번히 CRUD가 발생한다면 Cursor를 사용하면 좋을 것 같다.
그리고 이제 정렬 조건이 복잡해 Cursor의 성능이 저하되는 것 같은 상황이라면 LimitOffset, PageNumber 와 비교해서 테스트 해보고 각 상황에 어울리는 걸 고르면 될 것 같다.
offset이 크지 않고, 정적인 데이터라면 LimitOffset이나 PageNumber를 사용해도 좋을 것 같다.

## Reference
- [https://www.django-rest-framework.org/api-guide/pagination/#pagination](https://www.django-rest-framework.org/api-guide/pagination/#pagination)
