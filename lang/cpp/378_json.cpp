#include <format>
#include <print>
#include <string>
#include <type_traits>
#include <unordered_map>
#include <variant>
#include <vector>

class Json;

using JsonObject = std::unordered_map<std::string, Json>;
using JsonArray = std::vector<Json>;

class Json {
public:
    using value_type = std::variant<std::monostate, std::string, double, bool, JsonArray, JsonObject>;
    value_type value;

    Json() = default;

    template <class T>
    Json(T&& in)
        requires(std::is_constructible_v<value_type, T>)
        : value(std::forward<T>(in))
    {
    }
};

template <typename T>
std::string TypeWriter(T const& value)
{
    if constexpr (std::is_same_v<T, std::monostate>) {
        return "null";
    } else if constexpr (std::is_same_v<T, std::string>) {
        return std::format("\"{}\"", value);
    } else if constexpr (std::is_same_v<T, double>) {
        return std::format("{}", value);
    } else if constexpr (std::is_same_v<T, bool>) {
        return value ? "true" : "false";
    } else if constexpr (std::is_same_v<T, JsonArray>) {
        std::string result = "[";
        for (size_t i = 0; i < value.size() - 1; ++i) {
            result += SerializeJson(value.at(i));
            result += ", ";
        }
        if (!value.empty()) {
            result += SerializeJson(value.back());
        }
        result += "]";
        return result;
    } else if constexpr (std::is_same_v<T, JsonObject>) {
        std::string result = "{";
        size_t i = 0;
        for (auto const& [k, v] : value) {
            result += std::format("\"{}\": {}", k, SerializeJson(v));
            if (i != value.size() - 1) {
                result += ", ";
            }
        }
        result += "}";
        return result;
    } else {
        static_assert(false, "invalid type");
    }
}

std::string SerializeJson(Json const& json)
{
    return std::visit([](auto&& value) -> std::string {
        return TypeWriter(value);
    },
        json.value);
}

int main()
{
    auto value = Json(JsonArray { Json(), Json(123.0), JsonArray { Json("a"), Json("b"), Json(false) }, JsonObject { std::pair { "c", Json("d") } } });
    std::println("{}", SerializeJson(value));
}
