import { Test, TestingModule } from '@nestjs/testing';
import { NationsController } from './nations.controller';
import { NationsService } from './nations.service';

describe('NationsController', () => {
  let controller: NationsController;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [NationsController],
      providers: [NationsService],
    }).compile();

    controller = module.get<NationsController>(NationsController);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });
});
