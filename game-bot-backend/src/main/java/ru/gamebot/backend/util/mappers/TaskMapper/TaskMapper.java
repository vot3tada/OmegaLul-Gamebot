package ru.gamebot.backend.util.mappers.TaskMapper;

import org.mapstruct.InjectionStrategy;
import org.mapstruct.Mapper;
import ru.gamebot.backend.dto.TaskDTO;
import ru.gamebot.backend.models.Task;

@Mapper(
        componentModel = "spring",
        injectionStrategy = InjectionStrategy.CONSTRUCTOR
)
public interface TaskMapper {

    TaskDTO taskToTaskDTO(Task task);


    Task taskDTOToTask(TaskDTO taskDTO);
}
