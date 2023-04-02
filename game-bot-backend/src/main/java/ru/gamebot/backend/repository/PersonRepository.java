package ru.gamebot.backend.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import ru.gamebot.backend.models.Person;
import ru.gamebot.backend.models.PersonPK;

@Repository
public interface PersonRepository  extends JpaRepository<Person, PersonPK> {

}
