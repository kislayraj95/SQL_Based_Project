# Complete code
import sys
import datetime


def help(arg):
	sa = f"""Usage :-
 ===============COMMAND==============|||==DESCRIPTION=========
| python {arg} -a "todo item"     |   Add a new todo      |
| python {arg} -l                 |   Show TodoList       |
| python {arg} -d NUMBER          |   Delete a todo       |
| python {arg} -c NUMBER          |   Complete a todo     |
 ============================================================="""
	sys.stdout.buffer.write(sa.encode('utf8'))


def add(s):
	f = open('todo.txt', 'a')
	f.write("[ ]"+s)
	f.write("\n")
	f.close()
	s = '"'+s+'"'
	print(f"Added todo: {s}")


def display_list():
	try:
		read_history()
		if(len(todo_list) == 0):
			sys.stdout.buffer.write("List is empty\n".encode('utf8'))
			return

		index = 1;

		for i in todo_list:
			checked = todo_list[i][0]
			status = "[x]" if checked else "[ ]"
			sys.stdout.buffer.write(f"{index} - {status} {todo_list[i][1]}".encode('utf8'))
			sys.stdout.buffer.write("\n".encode('utf8'))
			index = index+1

	except Exception as e:
		raise e


def remove(index):
	try:
		index = int(index)
		if index not in todo_list.keys():
			print(f"todo {index} does not exist")
			return

		with open("todo.txt", "r") as f:
			lines = f.readlines()
			if len(lines) < 1: 
				print("Error: Todo is Empty")
				return
			ptr = 1
			with open('todo.txt', 'w') as fw:
				for line in lines:
               
					if ptr != index:
						fw.write(line)
					ptr += 1
		print(f"Deleted todo #{index}")

	except Exception as e:
		print(f"Error: todo at index {index} does not exist. Nothing deleted.")


def complete_task(index):
	try:
		index = int(index)
		if todo_list[index][0] == False:
			todo_list[index][0] = True

		with open("todo.txt", 'r+') as f:
			f.truncate()
			with open('todo.txt', 'w') as fw:
				for i in todo_list:
					checked = todo_list[i][0]
					status = "[x]" if checked else "[ ]"
					fw.write(status + todo_list[i][1] + "\n")

		print(f"Marked todo {index} as done")
	except:
		print(f"Error: todo number {index} does not exist.")



def read_history():
	try:
		f = open('todo.txt', 'r')
		c = 1
		for line in f:
			line = line.strip('\n')
			checked = False
			if(line[0:3] == "[x]"):
				checked = True
			elif(line[0:3] == "[ ]"):
				checked = False
			todo_list.update({c: [checked,line[3:]]})
			c = c+1
	except:
		sys.stdout.buffer.write("There are no pending todos!".encode('utf8'))


if __name__ == '__main__':
	todo_list = {}
	read_history()
	args = sys.argv
		
	if len(args) > 1:
		if(args[1] == '-a'):
			if(len(args[2:]) == 0):
				sys.stdout.buffer.write("Error: You must enter a string for adding a todo\n".encode('utf8'))
			else:
				add(*args[2:])
		elif(args[1] == '-r'):
			if(len(args[2:]) == 0):
				sys.stdout.buffer.write("Error: You must enter the index of the todo to be removed\n".encode('utf8'))
			else:
				remove(args[2])

		elif(args[1] == '-c'):
			if(len(args[2:]) == 0):
				sys.stdout.buffer.write("Error: Enter a task number to complete\n".encode('utf8'))
			else:
				if isinstance(int(args[2]), int):
					complete_task(args[2])
				else:
					sys.stdout.buffer.write("Unable to check: index is not a number\n".encode('utf8'))

		
		elif(args[1] == '-l'):
			display_list()


		elif(args[1] == "-h"):
			help(args[0])
		else:
			print("invalid syntax. type: 'todo -h'  for help")
	else:
		print("-------------Welcome to Todo--------------")	
		print("Use the following arguments to run a todo operation")	
		help(args[0])
		


		
