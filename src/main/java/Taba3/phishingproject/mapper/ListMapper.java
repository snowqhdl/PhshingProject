package Taba3.phishingproject.mapper;

import Taba3.phishingproject.dto.BlackListDto;
import Taba3.phishingproject.dto.PredictedListDto;
import Taba3.phishingproject.dto.WhiteListDto;
import Taba3.phishingproject.entity.BlackList;
import Taba3.phishingproject.entity.PredictedList;
import Taba3.phishingproject.entity.WhiteList;
import org.mapstruct.Mapper;

@Mapper(componentModel = "spring")
public interface ListMapper {
    BlackList postDtoToBlackList (BlackListDto.Post post);
    BlackListDto.Response blackListToResponse (BlackList blackList);

    WhiteList postDtoToWhiteList (WhiteListDto.Post post);
    WhiteListDto.Response whiteListToResponse (WhiteList whiteList);

    PredictedListDto.Response predictedListToResponse (PredictedList predictedList);
}
