from store.store_views import store

def register_blueprint(app):
    app.register_blueprint(store)

    return app
