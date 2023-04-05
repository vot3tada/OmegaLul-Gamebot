package ru.gamebot.backend.models;


import jakarta.persistence.Embeddable;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.io.Serializable;
import java.util.Objects;
@Embeddable
@Setter
@Getter
@AllArgsConstructor
@NoArgsConstructor
public class PersonPK implements Serializable {

    private int userId;

    private int chatId;

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        PersonPK personPK = (PersonPK) o;
        return userId == personPK.userId && chatId == personPK.chatId;
    }

    @Override
    public int hashCode() {
        return Objects.hash(userId, chatId);
    }
}
