package ru.gamebot.backend.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import ru.gamebot.backend.models.Item;
@Repository
public interface ItemRepository extends JpaRepository<Item, Integer> {

}
