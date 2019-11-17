var taskInput = document.getElementById("taskInput");
var timeInput = document.getElementById("timeInput");
var taskList = document.getElementById("taskList");
var timeList = document.getElementById("taskList");
var signUp = document.getElementById("signUp");
var add = document.getElementById("add");
var del = document.getElementById("delete");
var taskDict = {}; //task name: [task time, task num]
//var taskL = [];
//var timeL = [];
var dayInterval = [];
var taskCount = 0;
var phoneNum = document.getElementById("phoneNum").value;
var startTime = document.getElementById("startT").value;
var endTime = document.getElementById("endT").value;

add.addEventListener("click", add_activity);
del.addEventListener("click", del_activity);
signUp.addEventListener("click", takeUserInfo);



function add_activity(){
	taskCount += 1;
	taskDict[taskInput.value] = [timeInput.value, taskCount];
	//taskL.push(str(taskInput.value));
	//timeL.push(str(taskInput.value));
	//console.log(taskL);
	//console.log(timeL);
	var timenode = document.createElement("li");                 // Create a <li> node
	var tasknode = document.createElement("li");
	var timetextnode = document.createTextNode(timeInput.value);         // Create a text node
	var tasktextnode = document.createTextNode(taskInput.value);
	timenode.appendChild(timetextnode);                              // Append the text to <li>
	tasknode.appendChild(tasktextnode);
	taskList.appendChild(tasknode);
	timeList.appendChild(timenode);
	console.log(taskInput.value);
		//li.appendChild(document.createTextNode(String(newTask)));
	taskInput.reset();
	timeInput.reset();
	return false;
}

function del_activity(){
	taskList.removeChild(taskDict[taskInput.value][1]);           // Remove <ul>'s first child node (index 0)
	timeList.removeChild(taskDict[taskInput.value][1]);
	taskCount -= 1;
	delete taskDict[taskInput.value];
	taskInput.reset();
	timeInput.reset();
	return false;
}

function takeUserInfo(){
	dayInterval = [startTime, endTime];
}
