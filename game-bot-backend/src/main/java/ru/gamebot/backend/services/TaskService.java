package ru.gamebot.backend.services;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import ru.gamebot.backend.dto.TaskDTO;
import ru.gamebot.backend.dto.UpdateTaskDTO;
import ru.gamebot.backend.models.PersonPK;
import ru.gamebot.backend.models.Task;
import ru.gamebot.backend.repository.PersonRepository;
import ru.gamebot.backend.repository.TaskRepository;
import ru.gamebot.backend.util.exceptions.PersonExceptions.PersonNotFoundException;
import ru.gamebot.backend.util.exceptions.TaskExceptions.TaskNotFoundException;
import ru.gamebot.backend.util.mappers.TaskMapper.TaskMapper;

import java.util.ArrayList;
import java.util.List;

@Service
@Transactional(readOnly = true)
@RequiredArgsConstructor
public class TaskService {

    private final TaskRepository taskRepository;
    private final PersonRepository personRepository;
    private final TaskMapper taskMapper;

    public List<TaskDTO> allTasks(){
        var tasks = taskRepository.findAll();
        var tasksDTO = new ArrayList<TaskDTO>();
        for(Task task : tasks){
            tasksDTO.add(taskMapper.taskToTaskDTO(task));
        }
        return tasksDTO;
    }

    public List<TaskDTO> freeTasks(){
        var tasks = taskRepository.findTasksByWorkerUserIdIsNull();
        var tasksDTO = new ArrayList<TaskDTO>();
        for(Task task : tasks){
            tasksDTO.add(taskMapper.taskToTaskDTO(task));
        }
        return tasksDTO;
    }

    public List<TaskDTO> takenTasks(Integer workerUserId, Integer chatId){
        var tasks = taskRepository.findTasksByWorkerUserIdAndPersonPersonPkChatId(workerUserId, chatId);
        var tasksDTO = new ArrayList<TaskDTO>();
        for(Task task : tasks){
            tasksDTO.add(taskMapper.taskToTaskDTO(task));
        }
        return tasksDTO;
    }

    public List<TaskDTO> personTasks(Integer ownerUserId, Integer chatId){
        var tasks = taskRepository.findTasksByPersonPersonPk(new PersonPK(chatId, ownerUserId));
        var tasksDTO = new ArrayList<TaskDTO>();
        for(Task task : tasks){
            tasksDTO.add(taskMapper.taskToTaskDTO(task));
        }
        return tasksDTO;
    }

    @Transactional
    public void createTask(TaskDTO taskDTO){
        var person = personRepository.findById(new PersonPK(taskDTO.getChatId(),taskDTO.getOwnerUserId()))
                                                .orElseThrow(PersonNotFoundException::new);
        var task = taskMapper.taskDTOToTask(taskDTO);
        task.setPerson(person);
        taskRepository.save(task);
    }

    @Transactional
    public void updateTask(UpdateTaskDTO updateTaskDTO){
        var task = taskRepository.findById(updateTaskDTO.getId()).orElseThrow(TaskNotFoundException::new);
        task.setDeadline(updateTaskDTO.getDeadline());
        task.setWorkerUserId(updateTaskDTO.getWorkerUserId());
        taskRepository.save(task);
    }

    @Transactional
    public void taskDelete(Integer id){
        var task = taskRepository.findById(id).orElseThrow(TaskNotFoundException::new);
        taskRepository.delete(task);
    }
}
