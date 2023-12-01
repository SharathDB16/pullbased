import json

from flask import Flask, request, render_template


def read_result_configs():
    config_file = open("config.json")
    data = json.load(config_file)
    config_file.close()
    return data

app = Flask(__name__)

@app.errorhandler(404)
def special_search(error):
    full_path = request.full_path
    routes = full_path.split("?")[0].split("/")
    route = routes[1]
    sub_routes = routes[2:]
    request_args = dict(**request.args)
    configs = read_result_configs()
    route_config = configs.get(route, None)
    if not route_config or request.method not in route_config.get("methods", ["GET"]):
        print("route is %s, and sub routes are %s" %(route, str(sub_routes)), flush=True )
        return render_template("response404.json"), 404
    template =route_config.get("template", "response404.json")
    return_code = route_config.get("return_code", 404)
    jinja2 = route_config.get("jinja2", {})
    sub_route_names = route_config.get("sub_route_names",[])
    if len(sub_route_names) > len(sub_routes):
        return render_template("response404.json"), 404
    sub_route_dict = dict(zip(sub_route_names, sub_routes[:len(sub_route_names)]))
    request_args.update(sub_route_dict)
    request_args.update(jinja2)
    return render_template(template, **request_args), return_code


def main():
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host="0.0.0.0", port=80, debug=True)


if __name__ == "__main__":
   main()