class GenerateArray:
    def create_rooms(num_floors, rooms_per_floor):
        rooms = []
        room_number = 1  # Start with room number 1
        for floor in range(1, num_floors + 1):
            floor_rooms = []
            for room_num in range(1, rooms_per_floor + 1):
                room_data = [room_number, "Empty", f"Floor {floor}, Room {room_number}"]
                floor_rooms.append(room_data)
                room_number += 1  # Increment room number for the next room
            rooms.append(floor_rooms)
        return rooms

    def format_rooms(list_rooms):
        formatted_rooms = ""
        for floor_rooms in list_rooms:
            for room in floor_rooms:
                formatted_rooms += f"| {room[0]:<2} | {room[1]:<12} | {room[2]:<20} |\n"
            formatted_rooms += "+----+--------------+----------------------+\n"
        return formatted_rooms

    list_rooms = create_rooms(num_floors=4, rooms_per_floor=4)
    formatted_result = format_rooms(list_rooms)
    print(formatted_result)
