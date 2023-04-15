package ru.gamebot.backend.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import ru.gamebot.backend.models.PersonPK;
import ru.gamebot.backend.models.Task;

import java.util.List;

public interface TaskRepository extends JpaRepository<Task, Integer> {
    List<Task> findTasksByWorkerUserIdIsNull();

    List<Task> findTasksByWorkerUserIdAndPersonPersonPkChatId(Integer workerUserId, Integer chatId);

    List<Task> findTasksByPersonPersonPk(PersonPK personPK);
}
