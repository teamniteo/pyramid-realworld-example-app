"""Tests for Article related views."""

from conduit.auth.tests.test_auth_views import USER_TWO_JWT
from freezegun import freeze_time
from webtest import TestApp


@freeze_time("2019-01-01")
def test_GET_articles(testapp: TestApp, democontent: None) -> None:
    """Test GET /api/articles."""
    res = testapp.get("/api/articles", status=200)

    assert res.json == {
        "articlesCount": 2,
        "articles": [
            {
                "slug": "bar",
                "title": "Bär",
                "description": "Bär desc",
                "body": "Bär body",
                "createdAt": "2019-03-03T03:03:03.000003Z",
                "updatedAt": "2019-04-04T04:04:04.000004Z",
                "tagList": ["foo", "bar"],
                "favorited": False,
                "favoritesCount": 0,
                "author": {
                    "username": "one",
                    "bio": "",
                    "image": "",
                    "following": False,
                },
            },
            {
                "slug": "foo",
                "title": "Foö",
                "description": "Foö desc",
                "body": "Foö body",
                "createdAt": "2019-01-01T01:01:01.000001Z",
                "updatedAt": "2019-02-02T02:02:02.000002Z",
                "tagList": ["foo", "bar"],
                "favorited": False,
                "favoritesCount": 0,
                "author": {
                    "username": "one",
                    "bio": "",
                    "image": "",
                    "following": False,
                },
            },
        ],
    }


def test_GET_article(testapp: TestApp, democontent: None) -> None:
    """Test GET /api/article/{slug}."""
    res = testapp.get("/api/articles/foo", status=200)

    assert res.json == {
        "article": {
            "author": {"bio": "", "following": False, "image": "", "username": "one"},
            "body": "Foö body",
            "createdAt": "2019-01-01T01:01:01.000001Z",
            "description": "Foö desc",
            "favorited": False,
            "favoritesCount": 0,
            "slug": "foo",
            "tagList": ["foo", "bar"],
            "title": "Foö",
            "updatedAt": "2019-02-02T02:02:02.000002Z",
        }
    }


def test_GET_article_authenticated(testapp: TestApp, democontent: None) -> None:
    """Test GET /api/article/{slug}."""
    res = testapp.get(
        "/api/articles/foo",
        headers={"Authorization": f"Token {USER_TWO_JWT}"},
        status=200,
    )

    assert res.json == {
        "article": {
            "author": {"bio": "", "following": True, "image": "", "username": "one"},
            "body": "Foö body",
            "createdAt": "2019-01-01T01:01:01.000001Z",
            "description": "Foö desc",
            "favorited": False,
            "favoritesCount": 0,
            "slug": "foo",
            "tagList": ["foo", "bar"],
            "title": "Foö",
            "updatedAt": "2019-02-02T02:02:02.000002Z",
        }
    }


def test_POST_article(testapp: TestApp, democontent: None) -> None:
    """Test POST /api/articles."""
    res = testapp.post_json(
        "/api/articles",
        {
            "article": {
                "title": "A title",
                "description": "A description",
                "body": "A body",
                "taglist": ["one", "two"],
            }
        },
        headers={"Authorization": f"Token {USER_TWO_JWT}"},
        status=201,
    )

    assert res.json["article"]["author"]["username"] == "two"
    assert res.json["article"]["title"] == "A title"
    assert res.json["article"]["description"] == "A description"
    assert res.json["article"]["body"] == "A body"
    assert res.json["article"]["tagList"] == ["foo", "bar"]  # TODO: taglist support

    # TODO: mock createdAt and updatedAt to be able to compare entire output
    #     "article": {
    #         "author": {"bio": "", "following": True, "image": "", "username": "two"},
    #         "body": "A body",
    #         "createdAt": "2019-01-01T00:00:00Z",
    #         "description": "A description",
    #         "favorited": False,
    #         "favoritesCount": 0,
    #         "slug": "a-title",
    #         "tagList": ["foo", "bar"],  # TODO: taglist support
    #         "title": "A title",
    #         "createdAt": "2019-01-01T00:00:00Z",
    #     }
    # }
