cmake_minimum_required(VERSION 3.5)

project(edo_sim)

# Find dependencies
find_package(ament_cmake REQUIRED)

# Install directories (config, launch, meshes, robots)
install(DIRECTORY
	config
	launch
	meshes
	robots
	DESTINATION share/${PROJECT_NAME}
)

# ament package
ament_package()

