package ru.gamebot.backend.models;


import jakarta.persistence.Column;
import jakarta.persistence.Embeddable;
import lombok.*;

import java.io.Serializable;
import java.util.Objects;
@Embeddable
@Data
@NoArgsConstructor
public class PersonPK implements Serializable {

    @Column(name = "user_id")
    private int userId;
    @Column(name="chat_id")
    private int chatId;

    public PersonPK(int chatId, int userId){
        this.chatId=chatId;
        this.userId=userId;
    }
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
