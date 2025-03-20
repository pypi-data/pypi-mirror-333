-- handler.openresty
local jwt = require "resty.jwt"
local cjson = require "cjson"
local http = require "resty.http"

local function load_config()
    local lua_scripts_folder = os.getenv("LUA_SCRIPTS_FOLDER")
    if not lua_scripts_folder then
        error("Environment variable for Lua scripts folder is not set")
    end
    local config = dofile(lua_scripts_folder .. "/config.lua")
    return config
end

local function validate_jwt()
    local config = load_config()
    local headers = ngx.req.get_headers()
    local auth_header = headers["Authorization"]

    if not auth_header then
        ngx.status = ngx.HTTP_UNAUTHORIZED
        ngx.say("Unauthorized")
        return ngx.exit(ngx.HTTP_UNAUTHORIZED)
    end

    local _, _, token = string.find(auth_header, "Bearer%s+(.+)")

    if not token then
        ngx.status = ngx.HTTP_UNAUTHORIZED
        ngx.say("Unauthorized: Invalid Token Format")
        return ngx.exit(ngx.HTTP_UNAUTHORIZED)
    end

    local jwt_obj = jwt:verify(config.jwt_secret, token)
    if not jwt_obj["verified"] then
        ngx.status = ngx.HTTP_UNAUTHORIZED
        ngx.say("Invalid token")
        return false
    end

    local current_time = ngx.time()
    if jwt_obj.payload.exp and jwt_obj.payload.exp < current_time then
        ngx.status = ngx.HTTP_UNAUTHORIZED
        ngx.say("Token expired")
        return false
    end

    return jwt_obj.payload
end

local function proxy_request()
    local lab_id, rest_of_uri = ngx.var.uri:match("/api/(%w+)(.*)")
    local config = load_config()
    local port_map = config.port_map

    local url = port_map[lab_id]
    if not url then
        ngx.status = ngx.HTTP_NOT_FOUND
        ngx.say("Lab not found")
        return
    end

    local httpc = http.new()
    httpc:set_timeout(10000)
    local body
    if ngx.req.get_method() == "POST" then
        ngx.req.set_header("Content-Type", "application/json")
        ngx.req.read_body()
        body = ngx.req.get_body_data()
    end

    local res, err = httpc:request_uri(url .. rest_of_uri, {
        method = ngx.req.get_method(),
        headers = ngx.req.get_headers(),
        query = ngx.req.get_uri_args(),
        body = body,
        keepalive_timeout = 60,
        keepalive_pool = 10
    })

    if not res then
        ngx.status = ngx.HTTP_INTERNAL_SERVER_ERROR
        ngx.say("Failed to request: ", err)
        return
    end

    ngx.status = res.status
    ngx.say(res.body)
end

local payload = validate_jwt()
if payload then
    proxy_request()
end