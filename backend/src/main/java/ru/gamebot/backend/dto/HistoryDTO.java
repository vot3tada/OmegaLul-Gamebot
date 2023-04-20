package ru.gamebot.backend.dto;

import jakarta.validation.constraints.NotNull;
import lombok.Data;
import lombok.NoArgsConstructor;
import ru.gamebot.backend.models.HistoryPK;

@Data
@NoArgsConstructor
public class HistoryDTO {
    @NotNull
    private Integer chatId;
    @NotNull
    private Integer userId;
    @NotNull
    private Integer totalMoney;
    @NotNull
    private Integer totalExp;
    @NotNull
    private Integer totalQuestions;
    @NotNull
    private Integer totalFights;
    @NotNull
    private Integer totalWinFights;
    @NotNull
    private Integer totalWinBoss;
    @NotNull
    private Integer totalItem;
    @NotNull
    private Integer totalTakenTasks;
    @NotNull
    private Integer totalEndedTasks;
    @NotNull
    private Integer totalFallTasks;
    @NotNull
    private Integer totalWinCollector;
    @NotNull
    private Integer totalCreateEvent;
    @NotNull
    private Integer totalEnterEvent;
    @NotNull
    private Integer totalKickEvent;
    @NotNull
    private Integer totalLeaveFights;

    public HistoryPK toHistoryPK(){
        return new HistoryPK(this.userId,this.chatId);
    }
}
