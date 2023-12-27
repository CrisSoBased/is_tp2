import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { DatabaseModule } from './database/database.module';
import { PlayersController } from './players/players.controller';
import { PlayersService } from './players/players.service';
import { NationsController } from './nations/nations.controller';
import { ClubsController } from './clubs/clubs.controller';
import { NationsService } from './nations/nations.service';
import { ClubsService } from './clubs/clubs.service';

@Module({
  imports: [DatabaseModule],
  controllers: [AppController, PlayersController, NationsController, ClubsController],
  providers: [AppService, PlayersService, NationsService, ClubsService],
})
export class AppModule {}
