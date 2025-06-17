#define GLFW_INCLUDE_VULKAN
#include <GLFW/glfw3.h>

#include <cassert>
#include <stdexcept>
#include <vector>
#include <unordered_set>

// TODO: use vcpkg to manage GLFW / GLM dependencies
class HelloTriangle
{
public:
	static constexpr uint32_t WIDTH = 800;
	static constexpr uint32_t HEIGHT = 600;

	const std::vector<const char*> mValidationLayers = {
		"VK_LAYER_KHRONOS_validation"
	};

#ifdef NDEBUG
	constexpr static bool ENABLE_VALIDATION_LAYERS = false;
#else
	constexpr static bool ENABLE_VALIDATION_LAYERS = true;
#endif

	void run()
	{
		mainLoop();
	}

	HelloTriangle()
	{
		initWindow();
		initVulkan();
		assert(mWindow);
	}

	~HelloTriangle()
	{
		if (mInstance)
		{
			vkDestroyInstance(mInstance, nullptr);
		}
		if (mWindow)
		{
			glfwDestroyWindow(mWindow);
			glfwTerminate();
		}
	}
private:
	void initWindow()
	{
		glfwInit();
		glfwWindowHint(GLFW_CLIENT_API, GLFW_NO_API);
		glfwWindowHint(GLFW_RESIZABLE, GLFW_FALSE);
		mWindow = glfwCreateWindow(WIDTH, HEIGHT, "Vulkan", nullptr, nullptr);
	}

	void initVulkan()
	{
		createInstance();
		assert(mInstance);
	}

	void createInstance()
	{
		if (ENABLE_VALIDATION_LAYERS && !checkValidationLayerSupport())
		{
			throw std::runtime_error("validation layers requested, but not available!");
		}
		VkApplicationInfo appInfo{
			.sType = VK_STRUCTURE_TYPE_APPLICATION_INFO,
			.pApplicationName = "Hello Triangle",
			.applicationVersion = VK_MAKE_VERSION(1, 0, 0),
			.pEngineName = "No Engine",
			.engineVersion = VK_MAKE_VERSION(1, 0, 0),
			.apiVersion = VK_API_VERSION_1_0
		};
		uint32_t glfwExtensionCount = 0;
		const char** glfwExtensions = glfwGetRequiredInstanceExtensions(&glfwExtensionCount);
		VkInstanceCreateInfo createInfo{
			.sType = VK_STRUCTURE_TYPE_INSTANCE_CREATE_INFO,
			.pApplicationInfo = &appInfo,
			.enabledLayerCount = 0,
			.enabledExtensionCount = glfwExtensionCount,
			.ppEnabledExtensionNames = glfwExtensions
		};
		if (ENABLE_VALIDATION_LAYERS)
		{
			createInfo.enabledLayerCount = static_cast<uint32_t>(mValidationLayers.size());
			createInfo.ppEnabledLayerNames = mValidationLayers.data();
		}
		if (vkCreateInstance(&createInfo, nullptr, &mInstance) != VK_SUCCESS)
		{
			throw std::runtime_error("failed to create Vulkan instance!");
		}
	}

	bool checkValidationLayerSupport()
	{
		uint32_t layerCount;
		vkEnumerateInstanceLayerProperties(&layerCount, nullptr);
		std::vector<VkLayerProperties> availableLayers(layerCount);
		vkEnumerateInstanceLayerProperties(&layerCount, availableLayers.data());
		std::unordered_set<std::string> supportedLayers;
		for (const auto& layer : availableLayers)
		{
			supportedLayers.insert(layer.layerName);
		}
		for (const char* layerName : mValidationLayers)
		{
			if (!supportedLayers.contains(layerName))
			{
				return false;
			}
		}
		return true;
	}

	void mainLoop()
	{
		while (!glfwWindowShouldClose(mWindow))
		{
			glfwPollEvents();
		}
	}

	GLFWwindow* mWindow = nullptr;
	VkInstance mInstance = nullptr;
};

int main()
{
	HelloTriangle app;

	app.run();
}
