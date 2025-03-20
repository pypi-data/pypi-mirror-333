---
--- Created by yabian.
--- DateTime: 2025/3/5 14:47
---

-- local jwt = require "resty.jwt"
-- local cjson = require "cjson"
--
-- local jwt_secret = "your_secret_key"
--
-- local function generate_token()
--     local payload = {
--         user = "example_user",
--         exp = ngx.time() + 3600  -- token expiration time
--     }
--
--     local token = jwt:sign(jwt_secret, {
--         header = { typ = "JWT", alg = "HS256" },
--         payload = payload
--     })
--
--     ngx.say(cjson.encode({ token = token }))
-- end
--
-- generate_token()


--local jwt = require "resty.jwt"
--local cjson = require "cjson"
--
--local jwt_secret = "your_secret_key"
--local valid_key = "expected_key"
--local valid_secret = "expected_secret"
--
--local function generate_token()
--    -- 从头部获取密钥、密钥对和用户信息
--    local provided_key = ngx.req.get_headers()["X-API-Key"]
--    local provided_secret = ngx.req.get_headers()["X-API-Secret"]
--    local user = ngx.req.get_headers()["X-User"]
--
--    -- 验证提供的密钥和密钥对
--    if provided_key ~= valid_key or provided_secret ~= valid_secret then
--        ngx.status = ngx.HTTP_UNAUTHORIZED
--        ngx.say(cjson.encode({ error = "Unauthorized" }))
--        return
--    end
--
--    -- 如果验证成功，则生成令牌
--    local payload = {
--        user = user,  -- 使用动态传递的用户信息
--        exp = ngx.time() + 3600  -- 令牌过期时间
--    }
--
--    local token = jwt:sign(jwt_secret, {
--        header = { typ = "JWT", alg = "HS256" },
--        payload = payload
--    })
--
--    ngx.say(cjson.encode({ token = token }))
--end
--
--generate_token()

local jwt = require "resty.jwt"
local cjson = require "cjson"

local function load_config()
    local lua_scripts_folder = os.getenv("LUA_SCRIPTS_FOLDER")
    if not lua_scripts_folder then
        error("Environment variable for Lua scripts folder is not set")
    end
    local config = dofile(lua_scripts_folder .. "/config.lua")
    return config
end

local function is_valid_credential(provided_key, provided_secret, credentials)
    for _, cred in ipairs(credentials) do
        if cred.key == provided_key and cred.secret == provided_secret then
            return true
        end
    end
    return false
end

local function generate_token()
    -- Dynamically load config
    local config = load_config()

    -- Get key, secret, and user from headers
    local provided_key = ngx.req.get_headers()["X-API-Key"]
    local provided_secret = ngx.req.get_headers()["X-API-Secret"]
    local user = ngx.req.get_headers()["X-User"]

    -- Validate provided key and secret
    if not is_valid_credential(provided_key, provided_secret, config.credentials) then
        ngx.status = ngx.HTTP_UNAUTHORIZED
        ngx.say(cjson.encode({ error = "Unauthorized" }))
        return
    end

    -- Generate token if validation is successful
    local payload = {
        user = user,  -- Use dynamically passed user information
        exp = ngx.time() + 3600  -- Token expiration time
    }

    local token = jwt:sign(config.jwt_secret, {
        header = { typ = "JWT", alg = "HS256" },
        payload = payload
    })

    ngx.say(cjson.encode({ token = token }))
end

generate_token()