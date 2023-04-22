package ru.gamebot.backend.util.mappers;

import org.mapstruct.InjectionStrategy;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import ru.gamebot.backend.dto.TaskDTO;
import ru.gamebot.backend.models.Task;

@Mapper(
        componentModel = "spring",
        injectionStrategy = InjectionStrategy.CONSTRUCTOR
)
public interface TaskMapper {
    @Mapping(target = "chatId", expression = "java(task.getPerson().getPersonPk().getChatId())")
    @Mapping(target = "ownerUserId", expression = "java(task.getPerson().getPersonPk().getUserId())")
    TaskDTO taskToTaskDTO(Task task);


    Task taskDTOToTask(TaskDTO taskDTO);
}
