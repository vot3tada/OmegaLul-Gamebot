package ru.gamebot.backend.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import ru.gamebot.backend.models.History;
import ru.gamebot.backend.models.HistoryPK;

@Repository
public interface HistoryRepository extends JpaRepository<History, HistoryPK> {
}
