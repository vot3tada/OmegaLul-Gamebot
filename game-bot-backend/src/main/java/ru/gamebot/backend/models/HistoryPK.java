package ru.gamebot.backend.models;

import jakarta.persistence.Embeddable;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.io.Serializable;
import java.util.Objects;

@Embeddable
@Data
@NoArgsConstructor
public class HistoryPK implements Serializable {
    private Integer personUserId;
    private Integer personChatId;

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        HistoryPK historyPK = (HistoryPK) o;
        return Objects.equals(personUserId, historyPK.personUserId) && Objects.equals(personChatId, historyPK.personChatId);
    }

    @Override
    public int hashCode() {
        return Objects.hash(personUserId, personChatId);
    }

    public HistoryPK(Integer personUserId, Integer personChatId) {
        this.personUserId = personUserId;
        this.personChatId = personChatId;
    }
}
