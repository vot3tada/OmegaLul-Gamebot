package ru.gamebot.backend.services;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import ru.gamebot.backend.dto.TaskDTO;
import ru.gamebot.backend.models.PersonPK;
import ru.gamebot.backend.repository.PersonRepository;
import ru.gamebot.backend.repository.TaskRepository;
import ru.gamebot.backend.util.exceptions.PersonExceptions.PersonNotFoundException;
import ru.gamebot.backend.util.mappers.TaskMapper.TaskMapper;

@Service
@Transactional(readOnly = true)
@RequiredArgsConstructor
public class TaskService {

    private final TaskRepository taskRepository;
    private final PersonRepository personRepository;
    private final TaskMapper taskMapper;
    @Transactional
    public void createTask(TaskDTO taskDTO){
        var person = personRepository.findById(new PersonPK(taskDTO.getChatId(),taskDTO.getOwnerUserId()))
                                                .orElseThrow(PersonNotFoundException::new);
        var task = taskMapper.taskDTOToTask(taskDTO);
        task.setPerson(person);
        taskRepository.save(task);
    }
}
