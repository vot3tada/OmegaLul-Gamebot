package ru.gamebot.backend.dto;

import com.fasterxml.jackson.annotation.JsonFormat;
import jakarta.validation.constraints.Future;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
public class UpdateTaskDTO {
    private Integer id;
    private Integer workerUserId;

    @JsonFormat(pattern="yyyy-MM-dd HH:mm:ss")
    @Future
    private java.util.Date deadline;
}
