package ru.gamebot.backend.models;


import java.io.Serializable;
import java.util.Objects;

public class PersonPK implements Serializable {

    private int userId;

    private int chatId;

    public PersonPK(){

    }
    public PersonPK(int chatId, int userId){
        this.chatId = chatId;
        this.userId = userId;
    }
    public void setChatId(int chatId) {
        this.chatId = chatId;
    }

    public int getUserId() {
        return userId;
    }

    public void setUserId(int userId) {
        this.userId = userId;
    }

    public int getChatId() {
        return chatId;
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
