package ru.gamebot.backend.models;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;

@Entity
@Data
@NoArgsConstructor
public class History {
    @EmbeddedId
    private HistoryPK historyPK;
    private Integer totalMoney=0;
    private Integer totalExp=0;
    private Integer totalQuestions=0;
    private Integer totalFights=0;
    private Integer totalWinFights=0;
    private Integer totalWinBoss=0;
    private Integer totalItem=0;
    private Integer totalTakenTasks=0;
    private Integer totalEndedTasks=0;
    private Integer totalFallTasks=0;
    private Integer totalWinCollector=0;
    private Integer totalCreateEvent=0;
    private Integer totalEnterEvent=0;
    private Integer totalKickEvent=0;
    private Integer totalLeaveFights=0;
    private Integer totalCommits=0;
    private Integer totalMerges=0;
    @OneToOne
    @JoinColumns({@JoinColumn(name = "person_user_id", referencedColumnName = "user_id"), @JoinColumn(name="person_chat_id", referencedColumnName = "chat_id")})
    private Person person;

    public History(HistoryPK historyPK) {
        this.historyPK = historyPK;
    }
}
