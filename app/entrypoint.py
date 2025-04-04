from flask import redirect, url_for

if __name__ == '__main__':
    from app import init_app
    init_app() # initializes Flask app

    from app import ofp_app

    @ofp_app.route('/')
    def index():
        return redirect(url_for("dev.dev_index"))

    from dev import blueprint_dev
    # Page blueprints
    ofp_app.register_blueprint(blueprint_dev)

    # entrypoint
    ofp_app.run(debug=True, host='0.0.0.0')
