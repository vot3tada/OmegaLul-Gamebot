package ru.gamebot.backend.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import ru.gamebot.backend.models.Person;
import ru.gamebot.backend.models.PersonPK;

import java.util.List;

@Repository
public interface PersonRepository  extends JpaRepository<Person, PersonPK> {
    List<Person> findByPersonPkChatId(int chatId);
    long deletePersonByPersonPkChatId(int chatId);

}
