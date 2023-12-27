import { Module } from '@nestjs/common';
import { NationsService } from './nations.service';
import { NationsController } from './nations.controller';

@Module({
  controllers: [NationsController],
  providers: [NationsService],
})
export class NationsModule {}
